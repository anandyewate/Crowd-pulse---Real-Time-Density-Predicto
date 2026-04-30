import numpy as np

history = {}

def predict(cam_id, risk):
    if cam_id not in history:
        history[cam_id] = []
        
    hist = history[cam_id]
    hist.append(risk)

    if len(hist) > 30: # Use longer history for better regression
        hist.pop(0)

    # Need at least 10 points for a stable trend
    if len(hist) >= 10:
        x = np.arange(len(hist))
        y = np.array(hist)
        
        # Calculate Linear Regression Slope
        slope, intercept = np.polyfit(x, y, 1)
        
        # Trend classification
        if slope >= 0.4:
            return f"ACCELERATING SURGE (Slope: {slope:.2f})"
        elif slope >= 0.15:
            return "STEADY INCREASE"
        elif slope <= -0.2:
            return "DE-ESCALATING"
        elif abs(slope) < 0.05:
            return "STABLE"

    # Default logic for short history
    if risk >= 8:
        return "CRITICAL CAPACITY"
    elif risk >= 5:
        return "HIGH DENSITY"

    return "MONITORING"