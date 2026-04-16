from config import MAX_PEOPLE_PER_GRID

def calculate_risk(grid):
    total_cells = len(grid) * len(grid[0])

    overloaded_cells = 0
    total_excess = 0
    max_density = 0

    # 🔍 Analyze each grid cell
    for row in grid:
        for cell in row:
            max_density = max(max_density, cell)

            if cell > MAX_PEOPLE_PER_GRID:
                overloaded_cells += 1

                # how much over limit
                excess = cell - MAX_PEOPLE_PER_GRID
                total_excess += excess

    # 📊 Factor 1: % of overloaded zones
    overload_ratio = overloaded_cells / total_cells

    # 📊 Factor 2: how severe overload is
    if overloaded_cells > 0:
        avg_excess = total_excess / overloaded_cells
    else:
        avg_excess = 0

    # 🎯 FINAL RISK CALCULATION (weighted)
    risk = (overload_ratio * 6) + (avg_excess * 2)

    # Normalize to 0–10
    risk = min(risk, 10)

    # 🚦 LEVEL CLASSIFICATION
    if risk >= 8:
        level = "CRITICAL"
    elif risk >= 5:
        level = "CAUTION"
    else:
        level = "SAFE"

    return risk, level