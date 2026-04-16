import math

prev_positions = {}

def detect_panic(cam_id, detections):
    global prev_positions
    if cam_id not in prev_positions:
        prev_positions[cam_id] = []

    current = [(cx, cy) for x1, y1, x2, y2, cx, cy in detections]

    if not prev_positions[cam_id] or not current:
        prev_positions[cam_id] = current
        return False

    total_velocity = 0
    rapid_movers = 0
    
    for cx, cy in current:
        # Find the distance to the closest previous position
        min_dist = min([math.hypot(cx - px, cy - py) for px, py in prev_positions[cam_id]], default=0)
        
        # Filter noise and large jumps (new objects)
        if 15 < min_dist < 300: 
            total_velocity += min_dist
            
            # High threshold indicates rapid sprinting
            if min_dist > 60:
                rapid_movers += 1

    prev_positions[cam_id] = current

    # Panic condition: Highly chaotic swarm movement OR distinct sudden sprinters
    return total_velocity > 1800 or rapid_movers > 3