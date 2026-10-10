"""
========================================================================================
    Code for comparing grid-based and sampling-based path planning algorithms
========================================================================================
    Author: Jogesh S Nanda
    Created: 10/10/2026
    Modified: 10/10/2026    (by Jogesh S Nanda)
========================================================================================
    Code created for class of MN207 (by Robotics Innovations Lab,
        Department of Design and Manufacturing, IISc).

    version : Python 3, NumPy, Matplotlib

Purpose:
    To run Dijkstra, A*, RRT and RRT* on the same occupancy grid and visualize each path
========================================================================================
"""

"""
EXAMPLE 3: GRID PATH PLANNING ALGORITHMS
========================================

Run Dijkstra, A*, RRT and RRT* on the same sample occupancy grid.

The grid, start, goal and cell resolution belong to this example. Each
algorithm is imported as a reusable class, receives the same map inputs,
prints its path cost, and opens its own visualization window.
"""
import numpy as np
from importlib import import_module


# Load the reusable planner classes from the methods folder.
Dijkstra = import_module("methods.dijistra").Dijkstra
AStar = import_module("methods.Astar").AStar
RRT = import_module("methods.RRT").RRT
RRTStar = import_module("methods.RRTstar").RRTStar

# ==================================================
# STEP 1: DEFINE THE OCCUPANCY GRID
# ==================================================

# 0 = Free cell, which the robot can enter.
# 100 = Obstacle, which the robot must avoid.
# -1 = Unknown cell, treated as blocked by every planner.
grid = np.array([
    [0, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 100, 0, 0, 0, 0, 100, 0, 0, 0, 0, 100, 0, 0, 0, 0],
    [0, 0, 0, 0, 0,   0, 0, 0, 0, 0, 100, 0, 0, 0, 0, 100, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 100, 0, 0, 0, 0, 100, 0, 0, 0, 0,   0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 100, 0, 0, 0, 0, 100, 0, 0, 0, 0, 100, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 100, 0, 0, 0, 0, 100, 0, 0, 0, 0, 100, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 100, 0, 0, 0, 0,   0, 0, 0, 0, 0, 100, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 100, 0, 0, 0, 0, 100, 0, 0, 0, 0, 100, 0, 0, 0, 0],
    [0, 100, 100, 0, 100, 100, 100, 100, 0, 100, 100, 100, 100, 0, 100, 100, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 100, 0, 0, 0, 0, 100, 0, 0, 0, 0, 100, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 100, 0, 0, 0, 0, 100, 0, 0, 0, 0, 100, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 100, 0, 0, 0, 0, 100, 0, 0, 0, 0,   0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 100, 0, 0, 0, 0, 100, 0, 0, 0, 0, 100, 0, 0, 0, 0],
    [0, 0, 0, 0, 0,   0, 0, 0, 0, 0, 100, 0, 0, 0, 0, 100, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 100, 100, 100, 100, 0, 100, 100, 100, 100, 100, 100, 0, 100, 100, 0],
    [0, 0, 0, 0, 0, 100, 0, 0, 0, 0, 100, 0, 0, 0, 0, 100, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 100, 0, 0, 0, 0,   0, 0, 0, 0, 0, 100, 0, 0, 0, 0],
    [0, 0, 0, 0, 0,   0, 0, 0, 0, 0, 100, 0, 0, 0, 0,   0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0,   0, 0, 0, 0, 0, 100, 0, 0, 0, 0,   0, 0, 0, 0, 0]
], dtype=int)

# Starting and goal positions (row, column).
start = (1, 1)
goal = (18, 18)

# Physical size of one grid cell in meters. Grid path costs are converted
# to meters by multiplying the cost by this resolution.
resolution = 0.5


# ==================================================
# STEP 2: RUN DIJKSTRA'S SHORTEST PATH ALGORITHM
# ==================================================

if __name__ == "__main__":

    # Each planner receives the same map and start/goal coordinates.
    # Every visualize_path call opens a separate figure for comparison.

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

    # ==================================================
    # STEP 3: RUN A* SHORTEST PATH ALGORITHM
    # ==================================================

    astar_path, astar_cost = AStar.plan(
        grid,
        start,
        goal,
        verbose=True
    )

    # Print A* result
    if astar_path is not None:

        print("\n========== A* FINAL RESULT ==========")

        print("A* Shortest Path:")
        for point in astar_path:
            print(point, end=" -> ")
        print("END")

        print(f"\nGrid Steps: {astar_cost}")

        # Convert grid steps into meters
        astar_distance_m = astar_cost * resolution

        print(f"Path Length: {astar_distance_m:.2f} meters")

        # Display the A* path in a separate plot
        AStar.visualize_path(
            grid,
            astar_path,
            start,
            goal
        )

    # ==================================================
    # STEP 4: RUN RRT PATH PLANNING
    # ==================================================

    rrt_path, rrt_cost = RRT.plan(
        grid,
        start,
        goal,
        max_iterations=3000,
        step_size=1.0,
        goal_sample_rate=0.1,
        random_seed=7,
        verbose=True
    )

    # Print RRT result
    if rrt_path is not None:

        print("\n========== RRT FINAL RESULT ==========")

        print("RRT Path:")
        for point in rrt_path:
            print(tuple(round(value, 2) for value in point), end=" -> ")
        print("END")

        print(f"\nPath Length: {rrt_cost * resolution:.2f} meters")

        # Display the RRT path in a separate plot
        RRT.visualize_path(
            grid,
            rrt_path,
            start,
            goal
        )

    # ==================================================
    # STEP 5: RUN RRT* PATH PLANNING
    # ==================================================

    rrt_star_path, rrt_star_cost = RRTStar.plan(
        grid,
        start,
        goal,
        max_iterations=3000,
        step_size=1.0,
        goal_sample_rate=0.1,
        rewire_radius=2.5,
        random_seed=7,
        verbose=True
    )

    # Print RRT* result
    if rrt_star_path is not None:

        print("\n========== RRT* FINAL RESULT ==========")

        print("RRT* Path:")
        for point in rrt_star_path:
            print(tuple(round(value, 2) for value in point), end=" -> ")
        print("END")

        print(f"\nPath Length: {rrt_star_cost * resolution:.2f} meters")

        # Display the RRT* path in a separate plot
        RRTStar.visualize_path(
            grid,
            rrt_star_path,
            start,
            goal
        )
