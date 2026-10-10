
"""
========================================================================================
    Code for Dijkstra's algorithm for mobile robot path planning
========================================================================================
    Author: Jogesh S Nanda
    Created: 10/10/2026
    Modified: 10/10/2026    (by Jogesh S Nanda)
========================================================================================
    Code created for class of MN207 (by Robotics Innovations Lab,
        Department of Design and Manufacturing, IISc).

    version : Python 3, NumPy, Matplotlib

Purpose:
    To find and visualize the shortest collision-free path on an occupancy grid
========================================================================================
"""

"""
DIJKSTRA'S ALGORITHM FOR MOBILE ROBOT PATH PLANNING
=================================================

Occupancy grid:
    0   = Free cell
    100 = Obstacle
    -1  = Unknown cell (treated as obstacle)

Robot movement:
    Up, Down, Left, Right (4-connected grid)

Outputs:
    1. Shortest collision-free path
    2. Total path cost
    3. Distance matrix at every iteration
    4. Visited matrix at every iteration
    5. Parent matrix at every iteration
    6. Graphical path visualization
"""

import heapq
import math
import numpy as np
import matplotlib.pyplot as plt

from typing import Optional

# A grid position is represented as (row, column).
Cell = tuple[int, int]


# ==================================================
# STEP 1: DEFINE VALID ROBOT MOVEMENTS
# ==================================================

# Four-connected grid:
# Robot can move in four directions only.

DIRECTIONS = [
    (-1,  0),  # Up
    ( 1,  0),  # Down
    ( 0, -1),  # Left
    ( 0,  1)   # Right
]


# ==================================================
# STEP 2: PRINT SEARCH MATRICES
# ==================================================

def print_matrices(
    distance: np.ndarray,
    visited: np.ndarray,
    parent: np.ndarray,
    occupancy_grid: np.ndarray,
    iteration: int
) -> None:
    """
    Display the distance, visited and parent matrices
    after each Dijkstra iteration.
    """

    rows, cols = occupancy_grid.shape

    print(f"\n========== ITERATION {iteration} ==========")

    # ---------- Distance matrix ----------
    print("\nDistance Matrix D:")

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

            if occupancy_grid[r, c] != 0:
                value = "X"
            else:
                value = str(int(visited[r, c]))

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


# ==================================================
# STEP 3: DIJKSTRA'S SHORTEST PATH ALGORITHM
# ==================================================

class Dijkstra:
    """
    Find and display shortest paths on an occupancy grid.

    The grid, start and goal are provided by each example, so this
    planner can be reused with multiple maps. The search expands the
    lowest-cost unvisited cell and uses four-connected movement where
    every horizontal or vertical step costs one grid unit.
    """

    @staticmethod
    def plan(
        occupancy_grid: np.ndarray,
        start: Cell,
        goal: Cell,
        verbose: bool = True
    ) -> tuple[Optional[list[Cell]], float]:
        """
        Find the shortest collision-free path using Dijkstra.

        The priority queue selects the cell with the lowest known cost
        from the start. Each time a cheaper route to a neighbor is found,
        its distance and parent are updated. When the goal is finalized,
        the parent matrix is used to rebuild the path.

        Parameters
        ----------
        occupancy_grid : np.ndarray
            2D map where 0 is free. Nonzero values, including obstacles
            and unknown cells, are treated as blocked.

        start : tuple[int, int]
            Robot starting position (row, column).

        goal : tuple[int, int]
            Robot goal position (row, column).

        verbose : bool
            If True, print the distance, visited and parent matrices
            after each iteration.

        Returns
        -------
        path : list of (row, column) or None
            Shortest path from start to goal.

        cost : float
            Total path cost in grid steps.
        """

        rows, cols = occupancy_grid.shape

        # ---------- Check valid positions ----------

        for name, (r, c) in [
            ("Start", start),
            ("Goal", goal)
        ]:

            if not (0 <= r < rows and 0 <= c < cols):
                raise ValueError(f"{name} is outside the map")

            if occupancy_grid[r, c] != 0:
                raise ValueError(f"{name} is blocked")

        # ---------- Initialize distance matrix ----------

        # Every cell initially has infinite distance.
        distance = np.full(
            (rows, cols),
            math.inf,
            dtype=float
        )

        # ---------- Initialize visited matrix ----------

        # False means the shortest distance is not
        # finalized yet.
        visited = np.zeros(
            (rows, cols),
            dtype=bool
        )

        # ---------- Initialize parent matrix ----------

        # Parent stores the preceding node used to
        # reconstruct the path.
        parent = np.empty(
            (rows, cols),
            dtype=object
        )
        parent.fill(None)

        # Distance to starting node is zero.
        distance[start] = 0.0

        # ---------- Initialize priority queue ----------

        # Each entry contains:
        # (distance_from_start, row, column)
        #
        # heapq always removes the lowest-cost entry.
        priority_queue = [(0.0, start[0], start[1])]

        iteration = 0

        if verbose:
            print_matrices(
                distance, visited, parent,
                occupancy_grid, iteration
            )

        # ==================================================
        # MAIN DIJKSTRA SEARCH LOOP
        # ==================================================

        while priority_queue:

            # STEP A: Select node with minimum known cost
            current_cost, r, c = heapq.heappop(
                priority_queue
            )

            current: Cell = (r, c)

            # Ignore entries that were already finalized.
            if visited[current]:
                continue

            # STEP B: Finalize the current node
            visited[current] = True
            iteration += 1

            print(f"\nExpanding node: {current}")
            print(f"Current shortest cost: {current_cost}")

            # STEP C: Check whether the goal is reached
            if current == goal:

                print("\nGOAL REACHED!")

                if verbose:
                    print_matrices(
                        distance, visited, parent,
                        occupancy_grid, iteration
                    )

                break

            # STEP D: Explore all neighboring cells
            for dr, dc in DIRECTIONS:

                nr = r + dr
                nc = c + dc

                neighbor: Cell = (nr, nc)

                # Check whether neighbor is inside map
                if not (0 <= nr < rows and 0 <= nc < cols):
                    continue

                # Reject obstacles and unknown cells
                if occupancy_grid[neighbor] != 0:
                    continue

                # Ignore nodes already finalized
                if visited[neighbor]:
                    continue

                # STEP E: Calculate tentative travel cost

                # Each horizontal/vertical step costs 1.
                movement_cost = 1.0

                new_cost = (
                    distance[current] + movement_cost
                )

                # STEP F: Relax edge if cheaper path exists
                if new_cost < distance[neighbor]:

                    # Update shortest known distance
                    distance[neighbor] = new_cost

                    # Store predecessor of neighbor
                    parent[neighbor] = current

                    # Insert updated neighbor into queue
                    heapq.heappush(
                        priority_queue,
                        (new_cost, nr, nc)
                    )

                    print(
                        f"  Updated {neighbor}: "
                        f"distance = {new_cost}, "
                        f"parent = {current}"
                    )

            # STEP G: Display updated search matrices
            if verbose:
                print_matrices(
                    distance, visited, parent,
                    occupancy_grid, iteration
                )

        # ==================================================
        # STEP 4: CHECK IF A PATH WAS FOUND
        # ==================================================

        # Keep the final distance matrix for the path plot. Each free cell
        # will display its lowest known cost g from the start; cells that
        # were not reached keep an infinite cost.
        Dijkstra.last_cost_map = distance.copy()

        if not visited[goal]:

            print("No collision-free path found.")
            return None, math.inf

        # ==================================================
        # STEP 5: RECONSTRUCT OPTIMAL PATH
        # ==================================================

        path: list[Cell] = []

        current = goal

        # Follow parent pointers backward to start.
        while current is not None:

            path.append(current)
            current = parent[current]

        # Reverse to obtain Start -> Goal.
        path.reverse()

        return path, float(distance[goal])


# ==================================================
# STEP 6: VISUALIZE THE SHORTEST PATH
# ==================================================

def visualize_path(
    occupancy_grid: np.ndarray,
    path: Optional[list[Cell]],
    start: Cell,
    goal: Cell
) -> None:
    """
    Display obstacles, start, goal, cell costs and Dijkstra's path.

    Each free cell is labeled with its lowest known cost g from start.
    Unreached free cells show inf, while occupied and unknown cells show X.
    """

    rows, cols = occupancy_grid.shape

    fig, ax = plt.subplots(figsize=(7, 7))

    # Convert all occupied or unknown cells to 1 for display:
    # 0 = free cell, 1 = blocked cell.
    display_map = (occupancy_grid != 0).astype(int)

    ax.imshow(
        display_map,
        cmap="gray_r",
        vmin=0,
        vmax=1,
        origin="upper"
    )

    # Draw grid lines at cell boundaries.
    ax.set_xticks(
        np.arange(-0.5, cols, 1),
        minor=True
    )
    ax.set_yticks(
        np.arange(-0.5, rows, 1),
        minor=True
    )

    ax.grid(
        which="minor",
        color="gray",
        linewidth=0.8
    )

    # Plot the final route from start to goal.
    if path:

        path_rows = [cell[0] for cell in path]
        path_cols = [cell[1] for cell in path]

        ax.plot(
            path_cols,
            path_rows,
            "b-o",
            linewidth=3,
            markersize=6,
            label="Shortest Path"
        )

    # Mark robot start position
    ax.scatter(
        start[1], start[0],
        color="green",
        s=220,
        marker="s",
        label="Start",
        zorder=5
    )

    # Mark destination
    ax.scatter(
        goal[1], goal[0],
        color="red",
        s=220,
        marker="*",
        label="Goal",
        zorder=5
    )

    # Show the Dijkstra cost at every free cell instead of its coordinates.
    cost_map = getattr(Dijkstra, "last_cost_map", None)
    for r in range(rows):
        for c in range(cols):

            if occupancy_grid[r, c] != 0:
                label = "X"
                text_color = "white"
            elif cost_map is None:
                label = "--"
                text_color = "black"
            elif np.isinf(cost_map[r, c]):
                label = "inf"
                text_color = "black"
            else:
                label = f"{cost_map[r, c]:g}"
                text_color = "black"

            ax.text(
                c, r, label,
                ha="center",
                va="center",
                fontsize=8,
                color=text_color,
                zorder=6
            )

    ax.set_title(
        "Dijkstra Path Planning - g Cost per Cell",
        fontsize=14
    )

    ax.set_xlabel("Grid Column")
    ax.set_ylabel("Grid Row")

    ax.set_xticks(np.arange(cols))
    ax.set_yticks(np.arange(rows))

    ax.legend(loc="upper right")

    plt.tight_layout()
    plt.show()


Dijkstra.visualize_path = staticmethod(visualize_path)

