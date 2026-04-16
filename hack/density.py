def get_density(frame, detections, grid_size):
    h, w, _ = frame.shape
    grid = [[0]*grid_size for _ in range(grid_size)]

    cw = w//grid_size
    ch = h//grid_size

    for (_,_,_,_,cx,cy) in detections:
        col = min(cx//cw, grid_size-1)
        row = min(cy//ch, grid_size-1)
        grid[row][col] += 1

    return grid