import math
import numpy as np

# track_id -> (last_cx, last_cy, velocity_vector)
history = {}

def detect_panic(cam_id, detections):
    global history
    if cam_id not in history:
        history[cam_id] = {}

    current_history = history[cam_id]
    vectors = []
    rapid_movers = 0
    total_speed = 0

    # Process detections with track_ids
    active_ids = set()
    for x1, y1, x2, y2, cx, cy, track_id in detections:
        if track_id == -1: continue
        active_ids.add(track_id)
        
        if track_id in current_history:
            prev_x, prev_y = current_history[track_id]
            dx = cx - prev_x
            dy = cy - prev_y
            speed = math.hypot(dx, dy)
            
            # Filter noise
            if 10 < speed < 300:
                vectors.append((dx, dy))
                total_speed += speed
                if speed > 60:
                    rapid_movers += 1
        
        current_history[track_id] = (cx, cy)

    # Cleanup old tracks
    history[cam_id] = {tid: val for tid, val in current_history.items() if tid in active_ids}

    # Calculate Vector Entropy (Chaos)
    entropy = 0
    if len(vectors) > 4:
        # Angles of movement
        angles = [math.atan2(dy, dx) for dx, dy in vectors]
        # Standard deviation of angles indicates chaos
        entropy = np.std(angles)

    # Return combined risk: 
    # 1. High total speed (stampede)
    # 2. Chaos/Entropy (panic swarm)
    # 3. Individual sprinters
    is_panic = total_speed > 2500 or (entropy > 1.2 and len(vectors) > 10) or rapid_movers > 4
    
    # Return both panic state and the chaos score for telemetry
    return is_panic, round(entropy, 2)