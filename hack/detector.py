# Global model removed to fix multi-camera tracking ID collisions
from ultralytics import YOLO

def detect_people(frame, model):
    # Use persistent tracking
    results = model.track(frame, persist=True, verbose=False, tracker="botsort.yaml")
    detections = []

    for r in results:
        if r.boxes.id is not None:
            boxes = r.boxes.xyxy.cpu().numpy().astype(int)
            ids = r.boxes.id.cpu().numpy().astype(int)
            for box, track_id in zip(boxes, ids):
                x1, y1, x2, y2 = box
                cx, cy = (x1 + x2)//2, (y1 + y2)//2
                detections.append((x1, y1, x2, y2, cx, cy, track_id))
            return detections # Exit early if tracking is active

    # Fallback to normal detection if no tracks
    for r in results:
        for box in r.boxes:
            if int(box.cls[0]) == 0:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cx, cy = (x1 + x2)//2, (y1 + y2)//2
                detections.append((x1, y1, x2, y2, cx, cy, -1))

    return detections