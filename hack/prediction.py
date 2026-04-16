history = {}

def predict(cam_id, risk):
    if cam_id not in history:
        history[cam_id] = []
        
    hist = history[cam_id]
    hist.append(risk)

    if len(hist) > 15:
        hist.pop(0)

    if len(hist) >= 15:
        velocity = hist[-1] - hist[0]
        
        if velocity >= 3.5:
            return "RAPID SURGE PREDICTED"
        elif velocity >= 1.5:
            return "INCREASING TREND"
        elif velocity <= -2.0:
            return "DISPERSING"

    if risk >= 8:
        return "CRITICAL CAPACITY"
    elif risk >= 5:
        return "MODERATE CROWD"

    return "STABLE"