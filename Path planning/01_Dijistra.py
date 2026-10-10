
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
    Find and display the shortest paths on an occupancy grid.

    The grid, start and goal are provided by each example so the
    same planner can be reused with multiple maps.
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

        Parameters
        ----------
        occupancy_grid : np.ndarray
            2D map containing free and occupied cells.

        start : tuple[int, int]
            Robot starting position (row, column).

        goal : tuple[int, int]
            Robot goal position (row, column).

        verbose : bool
            If True, print matrices after each iteration.

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
        # STEP 5: CHECK IF A PATH WAS FOUND
        # ==================================================

        if not visited[goal]:

            print("No collision-free path found.")
            return None, math.inf

        # ==================================================
        # STEP 6: RECONSTRUCT OPTIMAL PATH
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
# STEP 4: VISUALIZE THE SHORTEST PATH
# ==================================================

def visualize_path(
    occupancy_grid: np.ndarray,
    path: Optional[list[Cell]],
    start: Cell,
    goal: Cell
) -> None:
    """
    Display obstacles, robot start, goal and
    Dijkstra's shortest path.
    """

    rows, cols = occupancy_grid.shape

    fig, ax = plt.subplots(figsize=(7, 7))

    # Create a numerical visualization map:
    # 0 = free, 1 = obstacle
    display_map = (occupancy_grid != 0).astype(int)

    ax.imshow(
        display_map,
        cmap="gray_r",
        vmin=0,
        vmax=1,
        origin="upper"
    )

    # Draw grid lines
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

    # Plot final shortest path
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

    # Add labels for each grid cell
    for r in range(rows):
        for c in range(cols):

            if occupancy_grid[r, c] != 0:
                label = "X"
                text_color = "white"
            else:
                label = f"({r},{c})"
                text_color = "black"

            # Avoid drawing labels over start/goal
            if (r, c) not in (start, goal):
                ax.text(
                    c, r, label,
                    ha="center",
                    va="center",
                    fontsize=9,
                    color=text_color
                )

    ax.set_title(
        "Dijkstra Path Planning - Occupancy Grid",
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

