"""
========================================================================================
    Code for A* algorithm for mobile robot path planning
========================================================================================
    Author: Jogesh S Nanda
    Created: 10/10/2026
    Modified: 10/10/2026    (by Jogesh S Nanda)
========================================================================================
    Code created for class of MN207 (by Robotics Innovations Lab,
        Department of Design and Manufacturing, IISc).

    version : Python 3, NumPy, Matplotlib

Purpose:
    To find and visualize a shortest collision-free path using g-cost and heuristic cost
========================================================================================
"""

"""
A* ALGORITHM FOR MOBILE ROBOT PATH PLANNING
===========================================

Occupancy grid:
    0   = Free cell
    100 = Obstacle
    -1  = Unknown cell (treated as obstacle)

Robot movement:
    Up, Down, Left, Right (4-connected grid)

Outputs:
    1. Shortest collision-free path
    2. Total path cost
    3. Distance, visited and parent matrices at every iteration
    4. Graphical path visualization

A* cost values:
    g = Known path cost from the start to the current cell
    h = Estimated remaining cost from the current cell to the goal
    f = g + h (the value used to order the search)

The Manhattan distance is used for h because the robot uses
four-connected movement and each move has a cost of 1.
"""

import heapq
import math
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np

# A grid position is represented as (row, column).
Cell = tuple[int, int]

# Four-connected grid:
# Robot can move in four directions only.
DIRECTIONS = [
    (-1,  0),  # Up
    ( 1,  0),  # Down
    ( 0, -1),  # Left
    ( 0,  1)   # Right
]


# ==================================================
# STEP 1: A* SHORTEST PATH ALGORITHM
# ==================================================

class AStar:
    """
    Find and display shortest paths on an occupancy grid using A*.

    The map, start and goal are supplied by the calling example. This
    lets the same planner work with multiple occupancy grids.
    """

    @staticmethod
    def _print_matrices(
        distance: np.ndarray,
        visited: np.ndarray,
        parent: np.ndarray,
        occupancy_grid: np.ndarray,
        iteration: int
    ) -> None:
        """
        Display the distance, visited and parent matrices after an iteration.

        Occupied and unknown cells are shown as X. Unvisited cells have
        an infinite distance, and parent entries show the preceding cell.
        """

        rows, cols = occupancy_grid.shape

        print(f"\n========== ITERATION {iteration} ==========")

        # ---------- Distance matrix ----------
        print("\nDistance Matrix G:")
        for r in range(rows):
            for c in range(cols):
                if occupancy_grid[r, c] != 0:
                    value = "X"
                elif math.isinf(distance[r, c]):
                    value = "inf"
                else:
                    value = str(int(distance[r, c]))
                print(f"{value:>5}", end="")
            print()

        # ---------- Visited matrix ----------
        print("\nVisited Matrix V:")
        for r in range(rows):
            for c in range(cols):
                value = "X" if occupancy_grid[r, c] != 0 else str(int(visited[r, c]))
                print(f"{value:>5}", end="")
            print()

        # ---------- Parent matrix ----------
        print("\nParent Matrix P:")
        for r in range(rows):
            for c in range(cols):
                if occupancy_grid[r, c] != 0:
                    value = "X"
                elif parent[r, c] is None:
                    value = "-"
                else:
                    pr, pc = parent[r, c]
                    value = f"{pr},{pc}"
                print(f"{value:>7}", end="")
            print()

    @staticmethod
    def _heuristic(current: Cell, goal: Cell) -> int:
        """
        Return the Manhattan distance for four-connected movement.

        This estimate adds the row and column differences. It never
        overestimates the remaining number of moves on this grid.
        """
        return abs(current[0] - goal[0]) + abs(current[1] - goal[1])

    @staticmethod
    def plan(
        occupancy_grid: np.ndarray,
        start: Cell,
        goal: Cell,
        verbose: bool = True
    ) -> tuple[Optional[list[Cell]], float]:
        """
        Find the shortest collision-free path using A*.

        The search expands the reachable cell with the lowest estimated
        total cost f = g + h. Once the goal is expanded, its shortest path
        is reconstructed by following the stored parent cells.

        Parameters
        ----------
        occupancy_grid : np.ndarray
            2D map containing free and occupied cells.

        start : tuple[int, int]
            Robot starting position (row, column).

        goal : tuple[int, int]
            Robot goal position (row, column).

        verbose : bool
            If True, print the search matrices after each iteration.

        Returns
        -------
        path : list of (row, column) or None
            Shortest path from start to goal.

        cost : float
            Total path cost in grid steps.
        """

        # ---------- Check the occupancy grid ----------
        if occupancy_grid.ndim != 2 or occupancy_grid.size == 0:
            raise ValueError("Occupancy grid must be a non-empty 2D array")

        rows, cols = occupancy_grid.shape

        # ---------- Check valid positions ----------
        for name, (r, c) in [("Start", start), ("Goal", goal)]:
            if not (0 <= r < rows and 0 <= c < cols):
                raise ValueError(f"{name} is outside the map")
            if occupancy_grid[r, c] != 0:
                raise ValueError(f"{name} is blocked")

        # ---------- Initialize search matrices ----------
        # g-cost stores the cheapest known cost from start to each cell.
        distance = np.full((rows, cols), math.inf, dtype=float)

        # A cell becomes visited after its cheapest route is finalized.
        visited = np.zeros((rows, cols), dtype=bool)

        # Parent stores the previous cell used to reach each cell.
        parent = np.empty((rows, cols), dtype=object)
        parent.fill(None)
        distance[start] = 0.0

        # Each queue entry contains:
        # (estimated_total_cost, actual_cost, row, column).
        # The heuristic makes the queue prefer cells estimated to be nearer
        # to the goal, while the g-cost preserves the path cost so far.
        priority_queue = [(float(AStar._heuristic(start, goal)), 0.0, start[0], start[1])]
        iteration = 0

        if verbose:
            AStar._print_matrices(distance, visited, parent, occupancy_grid, iteration)

        # ==================================================
        # MAIN A* SEARCH LOOP
        # ==================================================
        while priority_queue:
            estimated_cost, current_cost, r, c = heapq.heappop(priority_queue)
            current: Cell = (r, c)

            # A better route may have replaced a queued route, leaving an
            # outdated entry in the heap. Skip it and any finalized cell.
            if visited[current] or current_cost != distance[current]:
                continue

            # Finalize this cell: with the Manhattan heuristic, the first
            # time it is removed with its current best cost is optimal.
            visited[current] = True
            iteration += 1

            print(f"\nExpanding node: {current}")
            print(f"Current path cost: {current_cost}")
            print(f"Estimated total cost: {estimated_cost}")

            # Stop when the goal is reached. Its cost is now finalized.
            if current == goal:
                print("\nGOAL REACHED!")
                if verbose:
                    AStar._print_matrices(distance, visited, parent, occupancy_grid, iteration)
                break

            # ---------- Explore neighboring cells ----------
            for dr, dc in DIRECTIONS:
                nr = r + dr
                nc = c + dc
                neighbor: Cell = (nr, nc)

                # Reject cells outside the map, obstacles, and finalized cells.
                if not (0 <= nr < rows and 0 <= nc < cols):
                    continue
                if occupancy_grid[neighbor] != 0 or visited[neighbor]:
                    continue

                # Every horizontal or vertical step costs 1. Calculate the
                # candidate g-cost, then relax the cell if this route is cheaper.
                new_cost = current_cost + 1.0

                # Update the node when a cheaper path is found.
                if new_cost < distance[neighbor]:
                    distance[neighbor] = new_cost
                    parent[neighbor] = current
                    heuristic = AStar._heuristic(neighbor, goal)
                    heapq.heappush(
                        priority_queue,
                        (new_cost + heuristic, new_cost, nr, nc)
                    )
                    print(
                        f"  Updated {neighbor}: "
                        f"g = {new_cost}, h = {heuristic}, f = {new_cost + heuristic}, "
                        f"parent = {current}"
                    )

            if verbose:
                AStar._print_matrices(distance, visited, parent, occupancy_grid, iteration)

        # ==================================================
        # STEP 2: CHECK AND RECONSTRUCT THE PATH
        # ==================================================
        # The A* cost function is f = g + h. Save this final cost for every
        # cell so the plot can show the same value used to prioritize search.
        heuristic_map = np.fromfunction(
            lambda r, c: abs(r - goal[0]) + abs(c - goal[1]),
            (rows, cols),
            dtype=float
        )
        AStar.last_cost_map = distance + heuristic_map

        if not visited[goal]:
            print("No collision-free path found.")
            return None, math.inf

        path: list[Cell] = []
        current: Optional[Cell] = goal

        # Follow parent pointers backward from goal to start.
        while current is not None:
            path.append(current)
            current = parent[current]

        # Reverse the parent chain to obtain Start -> Goal.
        path.reverse()
        return path, float(distance[goal])

    # ==================================================
    # STEP 3: VISUALIZE THE SHORTEST PATH
    # ==================================================

    @staticmethod
    def visualize_path(
        occupancy_grid: np.ndarray,
        path: Optional[list[Cell]],
        start: Cell,
        goal: Cell
    ) -> None:
        """
        Display obstacles, robot start, goal, A* costs and the path.

        Each free cell is labeled with f = g + h, where g is the known cost
        from start and h is Manhattan distance to goal. Unreached cells show
        inf, while occupied and unknown cells show X.
        """

        rows, cols = occupancy_grid.shape
        fig, ax = plt.subplots(figsize=(7, 7))
        display_map = (occupancy_grid != 0).astype(int)

        ax.imshow(display_map, cmap="gray_r", vmin=0, vmax=1, origin="upper")
        ax.set_xticks(np.arange(-0.5, cols, 1), minor=True)
        ax.set_yticks(np.arange(-0.5, rows, 1), minor=True)
        ax.grid(which="minor", color="gray", linewidth=0.8)

        # Plot the final shortest path.
        if path:
            path_rows = [cell[0] for cell in path]
            path_cols = [cell[1] for cell in path]
            ax.plot(path_cols, path_rows, "m-o", linewidth=3, markersize=6, label="A* Path")

        # Mark robot start position and destination.
        ax.scatter(start[1], start[0], color="green", s=220, marker="s", label="Start", zorder=5)
        ax.scatter(goal[1], goal[0], color="red", s=220, marker="*", label="Goal", zorder=5)

        # Show the A* cost f = g + h at every cell instead of coordinates.
        cost_map = getattr(AStar, "last_cost_map", None)
        for r in range(rows):
            for c in range(cols):
                if occupancy_grid[r, c] != 0:
                    label, text_color = "X", "white"
                elif cost_map is None:
                    label, text_color = "--", "black"
                elif np.isinf(cost_map[r, c]):
                    label, text_color = "inf", "black"
                else:
                    label, text_color = f"{cost_map[r, c]:g}", "black"
                ax.text(
                    c, r, label,
                    ha="center",
                    va="center",
                    fontsize=8,
                    color=text_color,
                    zorder=6
                )

        ax.set_title("A* Path Planning - f = g + h per Cell", fontsize=14)
        ax.set_xlabel("Grid Column")
        ax.set_ylabel("Grid Row")
        ax.set_xticks(np.arange(cols))
        ax.set_yticks(np.arange(rows))
        ax.legend(loc="upper right")

        plt.tight_layout()
        plt.show()
