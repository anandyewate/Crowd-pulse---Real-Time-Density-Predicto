import cv2
import time
import threading
import os

from detector import detect_people
from density import get_density
from heatmap import apply_heatmap
from risk import calculate_risk
from movement import detect_panic
from prediction import predict
from alert import update_state, video_frames, frame_lock
from api import app
from nlp_engine import generate_assessment
from reid_engine import ReidExtractor
from config import GRID_SIZE, RISK_LIMIT, CAMERAS, MAX_PEOPLE_PER_GRID, NOTIFICATION_NUMBER


# Global ReID Engine
reid_engine = ReidExtractor()

class VideoGrabber:
    def __init__(self, src):
        self.cap = cv2.VideoCapture(src)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self.ret, self.frame = self.cap.read()
        self.running = True
        self.thread = threading.Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()

    def update(self):
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                self.ret, self.frame = ret, frame
            else:
                time.sleep(0.01)

    def read(self):
        return self.ret, self.frame

    def release(self):
        self.running = False
        self.cap.release()



def compute_dynamic_threshold(frame, people_count):
    h, w = frame.shape[:2]
    frame_area = h * w

    # 🔥 density-based threshold (adaptive)
    base_density = frame_area / 50000  # tuning factor
    threshold = max(3, int(base_density))

    # optional adjustment using current crowd
    threshold = max(threshold, int(people_count / 5) + 1)

    return threshold


def run_camera(cam):
    cam_id = cam["id"]
    src = cam["src"]
    loc = cam["loc"]

    from ultralytics import YOLO
    model = YOLO("yolov8n.pt")

    grabber = VideoGrabber(src)
    prev_time = time.time()
    trajectories = {} # track_id -> list of (x, y)
    reid_cache = {} # track_id -> {"emb": vector, "last_updated": frame_count}
    frame_count = 0
    total_processed = 0
    global reid_engine

    # Hold onto the last processed detections/grid for skipped frames
    last_detections = []
    last_grid = None
    last_panic, last_entropy = False, 0.0
    last_risk, last_level = 0.0, "SAFE"
    last_pred, last_ai_report = "STABLE", ""
    last_max_capacity = 0
    last_threshold = 0

    while True:
        ret, frame = grabber.read()

        if not ret:
            print(f"[WARN] {cam_id} disconnected. Reconnecting...")
            grabber.release()
            time.sleep(1)
            grabber = VideoGrabber(src)
            continue

        frame = cv2.resize(frame, (640, 480))

        current_time = time.time()
        fps = 1 / (current_time - prev_time + 1e-6)
        prev_time = current_time

        # ================= CORE =================
        frame_h, frame_w = frame.shape[:2]
        resolution_str = f"{frame_w}x{frame_h}"

        # 🚀 FRAME SKIPPING: Only run AI every 2nd frame to save CPU
        should_process = (frame_count % 2 == 0)

        if should_process:
            detections = detect_people(frame, model)
            last_detections = detections
            current_embeddings = []

            for d in detections:
                x1, y1, x2, y2, cx, cy, track_id = d
                
                # CPU OPTIMIZATION: Check cache first
                need_reid = False
                if track_id != -1:
                    if track_id not in reid_cache or (frame_count - reid_cache[track_id]["last_updated"] > 45):
                        need_reid = True
                
                if need_reid:
                    crop = frame[max(0, y1):min(frame_h, y2), max(0, x1):min(frame_w, x2)]
                    if crop.size > 0:
                        emb = reid_engine.get_embedding(crop)
                        if emb is not None:
                            reid_cache[track_id] = {"emb": emb, "last_updated": frame_count}
                
                if track_id in reid_cache:
                    current_embeddings.append(reid_cache[track_id]["emb"])

            grid = get_density(frame, detections, GRID_SIZE)
            last_grid = grid
            
            panic, entropy = detect_panic(cam_id, detections)
            risk, level = calculate_risk(grid)
            pred = predict(cam_id, risk)
            ai_report = generate_assessment(cam_id, len(detections), level, entropy, pred)
            
            people_count = len(detections)
            current_threshold = compute_dynamic_threshold(frame, people_count)
            max_capacity = int(GRID_SIZE * GRID_SIZE * current_threshold)
            
            last_panic, last_entropy = panic, entropy
            last_risk, last_level = risk, level
            last_pred, last_ai_report = pred, ai_report
            last_max_capacity, last_threshold = max_capacity, current_threshold
            
            update_state(cam_id, loc, people_count, fps, risk, panic, pred, max_capacity, resolution_str, entropy, ai_report, current_embeddings)
        else:
            detections = last_detections
            grid = last_grid
            panic, entropy = last_panic, last_entropy
            risk, level = last_risk, last_level
            pred = last_pred
            ai_report = last_ai_report
            max_capacity = last_max_capacity
            current_threshold = last_threshold
            people_count = len(detections)

        # Always apply visuals (on every frame)
        if last_grid is not None:
            frame = apply_heatmap(frame, last_grid)

        for d in detections:
            x1, y1, x2, y2, cx, cy, track_id = d
            color = (0, 255, 0) if track_id != -1 else (128, 128, 128)
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, f"ID:{track_id}", (x1, y1-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

            if track_id != -1:
                if track_id not in trajectories: trajectories[track_id] = []
                trajectories[track_id].append((cx, cy))
                if len(trajectories[track_id]) > 20: trajectories[track_id].pop(0)
                for i in range(1, len(trajectories[track_id])):
                    cv2.line(frame, trajectories[track_id][i-1], trajectories[track_id][i], (0, 255, 255), 1)

        people_count = len(detections)
        current_threshold = compute_dynamic_threshold(frame, people_count)
        max_capacity = GRID_SIZE * GRID_SIZE * current_threshold

        # ================= DISPLAY =================

        cv2.putText(frame, f"{cam_id} ({loc})", (20, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

        cv2.putText(frame, f"Risk: {risk:.1f} {level}", (20, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,255), 2)

        cv2.putText(frame, f"{pred}", (20, 110),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,255), 2)

        # color logic based on total screen capacity (not just per-grid limit)
        info_color = (0,255,0) if people_count <= max_capacity else (0,0,255)
        cv2.putText(frame, f"People: {people_count}", (20, 150),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, info_color, 2)

        cv2.putText(frame, f"Chaos Ind: {entropy}", (20, 190),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 100, 0), 2)

        if panic:
            cv2.putText(frame, "PANIC!", (20, 230),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)

        cv2.putText(frame, f"Capacity: {people_count}/{max_capacity}",
                    (20, 310), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,0), 2)

        # resolution bottom center
        res_size = cv2.getTextSize(resolution_str, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)[0]
        cv2.putText(frame, f"Res: {resolution_str}",
                    (frame_w // 2 - res_size[0] // 2, frame_h - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200,200,200), 1)

        # FPS
        fps_text = f"FPS: {int(fps)}"
        text_size = cv2.getTextSize(fps_text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)[0]
        cv2.putText(frame, fps_text,
                    (frame_w - text_size[0] - 20, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

        # Update global video frame for web streaming
        _, buffer = cv2.imencode('.jpg', frame)
        with frame_lock:
            video_frames[cam_id] = buffer.tobytes()

        cv2.imshow(f"CrowdPulse LIVE: {cam_id}", frame)

        if cv2.waitKey(1) == 27:
            grabber.release()
            import os
            os._exit(0)
            
        frame_count += 1

    grabber.release()


# ================= THREADS =================
threads = []

for cam in CAMERAS:
    t = threading.Thread(target=run_camera, args=(cam,))
    t.daemon = True
    t.start()
    threads.append(t)

# Run Flask in a separate thread so it doesn't block the main loop
def run_flask():
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)

flask_thread = threading.Thread(target=run_flask)
flask_thread.daemon = True
flask_thread.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopping...")

cv2.destroyAllWindows()