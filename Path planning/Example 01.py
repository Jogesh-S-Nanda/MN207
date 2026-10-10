"""
EXAMPLE 1: DIJKSTRA'S ALGORITHM
===============================

Plan a shortest path on a sample occupancy grid.
The grid and robot positions belong to this example, while the
Dijkstra class can be reused by other examples with different maps.
"""

import numpy as np

from importlib import import_module

Dijkstra = import_module("01_Dijistra").Dijkstra

# ==================================================
# STEP 1: DEFINE THE OCCUPANCY GRID
# ==================================================

# 0 = Free cell
# 100 = Obstacle
# -1 = Unknown cell (treated as obstacle)
grid = np.array([
    [0,   0,   0,   0, 0],
    [0, 100, 100,   0, 0],
    [0,   0, 100,   0, 0],
    [0, 100,   0,   0, 0],
    [0,   0,   0,   0, 0]
], dtype=int)

# Starting and goal positions (row, column)
start = (0, 0)
goal = (4, 4)

# Physical size of one grid cell in meters
resolution = 0.5


# ==================================================
# STEP 2: RUN DIJKSTRA'S SHORTEST PATH ALGORITHM
# ==================================================

if __name__ == "__main__":

    # Run Dijkstra's algorithm
    shortest_path, total_cost = Dijkstra.plan(
        grid,
        start,
        goal,
        verbose=True
    )

    # Print final result
    if shortest_path is not None:

        print("\n========== FINAL RESULT ==========")

        print("Shortest Path:")
        for point in shortest_path:
            print(point, end=" -> ")
        print("END")

        print(f"\nGrid Steps: {total_cost}")

        # Convert grid steps into meters
        distance_m = total_cost * resolution

        print(f"Path Length: {distance_m:.2f} meters")

        # Display planned path
        Dijkstra.visualize_path(
            grid,
            shortest_path,
            start,
            goal
        )
