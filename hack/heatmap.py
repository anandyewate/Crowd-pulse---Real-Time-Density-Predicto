import cv2
import numpy as np
from config import CRITICAL_THRESHOLD

def apply_heatmap(frame, grid):
    h, w, _ = frame.shape
    heat = np.zeros_like(frame)

    gs = len(grid)
    cw = w//gs
    ch = h//gs

    for i in range(gs):
        for j in range(gs):
            val = grid[i][j]

            if val >= CRITICAL_THRESHOLD:
                color = (0,0,255)
            elif val >= 2:
                color = (0,255,255)
            else:
                color = (0,255,0)

            x1, y1 = j*cw, i*ch
            x2, y2 = x1+cw, y1+ch

            cv2.rectangle(heat,(x1,y1),(x2,y2),color,-1)

    return cv2.addWeighted(frame,0.7,heat,0.3,0)