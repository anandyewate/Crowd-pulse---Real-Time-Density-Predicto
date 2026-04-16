import cv2
import time
import threading
from detector import detect_people
from density import get_density
from heatmap import apply_heatmap
from risk import calculate_risk
from movement import detect_panic
from prediction import predict
from alert import update_state
from config import GRID_SIZE, RISK_LIMIT, CAMERAS

def run_camera(cam):
    cam_id = cam["id"]
    src = cam["src"]
    loc = cam["loc"]
    
    cap = cv2.VideoCapture(src)
    prev_time = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            # Re-initialize feed if it drops (for mock feeds/videos)
            cap = cv2.VideoCapture(src)
            ret, frame = cap.read()
            if not ret: break # Break if still fails
            
        current_time = time.time()
        fps = 1 / (current_time - prev_time) if prev_time > 0 else 0
        prev_time = current_time

        detections = detect_people(frame)

        for (x1,y1,x2,y2,_,_) in detections:
            cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)

        grid = get_density(frame, detections, GRID_SIZE)
        frame = apply_heatmap(frame, grid)

        panic = detect_panic(cam_id, detections)
        risk, level = calculate_risk(grid)
        pred = predict(cam_id, risk)

        people_count = len(detections)
        update_state(cam_id, loc, people_count, fps, risk, panic, pred)

        cv2.putText(frame, f"Risk:{risk:.1f} {level}", (20,40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

        cv2.putText(frame, f"{pred}", (20,80),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)

        cv2.putText(frame, f"People: {len(detections)}", (20,160),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)
        
        if panic:
            cv2.putText(frame, "PANIC!", (20,120),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
                        
        # Display FPS in the top right corner
        fps_text = f"FPS: {int(fps)}"
        frame_h, frame_w = frame.shape[:2]
        text_size = cv2.getTextSize(fps_text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
        cv2.putText(frame, fps_text, (frame_w - text_size[0] - 20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow(f"CrowdPulse LIVE: {cam_id} ({loc})", frame)

        if cv2.waitKey(1) == 27:
            os._exit(0)

    cap.release()

threads = []
for cam in CAMERAS:
    t = threading.Thread(target=run_camera, args=(cam,))
    t.daemon = True
    t.start()
    threads.append(t)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass
    
cv2.destroyAllWindows()