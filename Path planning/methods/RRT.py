"""
========================================================================================
    Code for RRT algorithm for mobile robot path planning
========================================================================================
    Author: Jogesh S Nanda
    Created: 10/10/2026
    Modified: 10/10/2026    (by Jogesh S Nanda)
========================================================================================
    Code created for class of MN207 (by Robotics Innovations Lab,
        Department of Design and Manufacturing, IISc).

    version : Python 3, NumPy, Matplotlib

Purpose:
    To plan and visualize a collision-free path using a rapidly-exploring random tree
========================================================================================
"""

"""
RRT ALGORITHM FOR MOBILE ROBOT PATH PLANNING
============================================

Occupancy grid:
    0   = Free cell
    100 = Obstacle
    -1  = Unknown cell (treated as obstacle)

Outputs:
    1. Collision-free path from start to goal
    2. Total path length in grid units
    3. Graphical path visualization

RRT search process:
    1. Sample a free point (or sample the goal with a given probability).
    2. Find the nearest point already in the tree.
    3. Extend the tree toward the sample by at most one step size.
    4. Add the new point only when the connecting edge is collision-free.
    5. Stop when a tree point can safely connect to the goal.

The returned path uses floating-point (row, column) positions. Grid cell
centers use integer coordinates, and every edge is checked along its length.
"""

import math
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np

# A position is represented as (row, column).
Point = tuple[float, float]
Cell = tuple[int, int]


# ==================================================
# STEP 1: RRT PATH PLANNING
# ==================================================

class RRT:
    """
    Plan a collision-free path on an occupancy grid using RRT.

    RRT grows a tree from the start by adding safe, short connections
    toward random samples. The grid and positions are passed in by each
    example so this class can be reused with other maps.
    """

    @staticmethod
    def _distance(first: Point, second: Point) -> float:
        """
        Return Euclidean distance between two grid positions.

        RRT uses this distance to find the nearest tree node and to
        measure the length of each path segment.
        """
        return math.hypot(first[0] - second[0], first[1] - second[1])

    @staticmethod
    def _cell_is_free(occupancy_grid: np.ndarray, point: Point) -> bool:
        """
        Check whether a point lies inside a free grid cell.

        Adding 0.5 before flooring maps each integer-centered cell to
        the interval from -0.5 to +0.5 around its center.
        """
        rows, cols = occupancy_grid.shape
        r = int(math.floor(point[0] + 0.5))
        c = int(math.floor(point[1] + 0.5))
        return 0 <= r < rows and 0 <= c < cols and occupancy_grid[r, c] == 0

    @staticmethod
    def _edge_is_free(
        occupancy_grid: np.ndarray,
        first: Point,
        second: Point
    ) -> bool:
        """
        Check the full line between two points for obstacles.

        The segment is sampled every 0.1 grid units. A connection is
        accepted only when every sampled point maps to a free cell.
        """
        distance = RRT._distance(first, second)
        steps = max(1, math.ceil(distance / 0.1))
        for index in range(steps + 1):
            # Interpolate a point along the candidate edge.
            fraction = index / steps
            point = (
                first[0] + fraction * (second[0] - first[0]),
                first[1] + fraction * (second[1] - first[1])
            )
            if not RRT._cell_is_free(occupancy_grid, point):
                return False
        return True

    @staticmethod
    def _steer(first: Point, second: Point, step_size: float) -> Point:
        """
        Move from the nearest tree node toward a sampled point.

        If the sample is close, return it directly. Otherwise return the
        point exactly step_size units along the direction to the sample.
        """
        distance = RRT._distance(first, second)
        if distance <= step_size:
            return second
        scale = step_size / distance
        return (
            first[0] + scale * (second[0] - first[0]),
            first[1] + scale * (second[1] - first[1])
        )

    @staticmethod
    def _sample_free_point(
        occupancy_grid: np.ndarray,
        free_cells: list[Cell],
        rng: np.random.Generator
    ) -> Point:
        """
        Sample a point inside a randomly selected free cell.

        A small random offset around the cell center lets the tree grow
        in continuous coordinates while keeping samples away from cell
        boundaries.
        """
        r, c = free_cells[int(rng.integers(len(free_cells)))]
        return (
            r + float(rng.uniform(-0.4, 0.4)),
            c + float(rng.uniform(-0.4, 0.4))
        )

    @staticmethod
    def _cost_map_from_tree(
        occupancy_grid: np.ndarray,
        nodes: list[Point],
        costs: list[float]
    ) -> np.ndarray:
        """Map the lowest accumulated tree cost to each visited grid cell."""
        cost_map = np.full(occupancy_grid.shape, math.inf, dtype=float)
        for point, cost in zip(nodes, costs):
            r = int(math.floor(point[0] + 0.5))
            c = int(math.floor(point[1] + 0.5))
            if 0 <= r < occupancy_grid.shape[0] and 0 <= c < occupancy_grid.shape[1]:
                cost_map[r, c] = min(cost_map[r, c], cost)
        return cost_map

    @staticmethod
    def plan(
        occupancy_grid: np.ndarray,
        start: Cell,
        goal: Cell,
        max_iterations: int = 3000,
        step_size: float = 1.0,
        goal_sample_rate: float = 0.1,
        random_seed: Optional[int] = 0,
        verbose: bool = True
    ) -> tuple[Optional[list[Point]], float]:
        """
        Find a collision-free path using Rapidly-exploring Random Tree.

        The tree begins at start. Each iteration samples a target, extends
        the nearest node toward it, and adds the new node if the edge is
        clear. This version returns the first path that safely reaches goal.

        Parameters
        ----------
        occupancy_grid : np.ndarray
            2D map containing free and occupied cells.

        start : tuple[int, int]
            Robot starting position (row, column).

        goal : tuple[int, int]
            Robot goal position (row, column).

        max_iterations : int
            Maximum number of tree expansion attempts.

        step_size : float
            Maximum distance added to the tree in one expansion.

        goal_sample_rate : float
            Probability of sampling the goal directly, from 0 to 1.

        random_seed : int or None
            Seed for repeatable random sampling. None uses a random seed.

        verbose : bool
            If True, print search progress.

        Returns
        -------
        path : list of (row, column) or None
            Collision-free path from start to goal.

        cost : float
            Total path length in grid units.
        """

        # ---------- Check the map and planner settings ----------
        if occupancy_grid.ndim != 2 or occupancy_grid.size == 0:
            raise ValueError("Occupancy grid must be a non-empty 2D array")
        if max_iterations <= 0 or step_size <= 0:
            raise ValueError("max_iterations and step_size must be positive")
        if not 0.0 <= goal_sample_rate <= 1.0:
            raise ValueError("goal_sample_rate must be between 0 and 1")

        # ---------- Check that start and goal are valid free cells ----------
        rows, cols = occupancy_grid.shape
        for name, (r, c) in [("Start", start), ("Goal", goal)]:
            if not (0 <= r < rows and 0 <= c < cols):
                raise ValueError(f"{name} is outside the map")
            if occupancy_grid[r, c] != 0:
                raise ValueError(f"{name} is blocked")

        if start == goal:
            RRT.last_cost_map = np.full(occupancy_grid.shape, math.inf, dtype=float)
            RRT.last_cost_map[start] = 0.0
            return [(float(start[0]), float(start[1]))], 0.0

        # ---------- Prepare the random sampler and search tree ----------
        # Sampling starts from the centers of free cells. A small offset is
        # added by _sample_free_point when the sample is generated.
        free_cells = [
            (int(r), int(c))
            for r, c in np.argwhere(occupancy_grid == 0)
        ]
        if len(free_cells) < 2:
            return None, math.inf

        rng = np.random.default_rng(random_seed)
        start_point: Point = (float(start[0]), float(start[1]))
        goal_point: Point = (float(goal[0]), float(goal[1]))
        # nodes[i] stores a point in the tree. parents[i] stores the index
        # of the preceding point; the start has no parent.
        nodes: list[Point] = [start_point]
        parents: list[Optional[int]] = [None]
        costs = [0.0]

        # ==================================================
        # MAIN RRT SEARCH LOOP
        # ==================================================
        for iteration in range(1, max_iterations + 1):
            # Bias some samples directly toward the goal so the tree is
            # more likely to make progress in the goal's direction.
            if rng.random() < goal_sample_rate:
                sample = goal_point
            else:
                sample = RRT._sample_free_point(occupancy_grid, free_cells, rng)

            # Find the existing tree node closest to the sample.
            nearest_index = min(
                range(len(nodes)),
                key=lambda index: RRT._distance(nodes[index], sample)
            )
            # Extend from the nearest node by no more than step_size.
            new_point = RRT._steer(nodes[nearest_index], sample, step_size)

            # Reject this expansion if any part of its edge hits an obstacle.
            if not RRT._edge_is_free(occupancy_grid, nodes[nearest_index], new_point):
                continue

            # Add the new point and record the edge that connects it to the tree.
            nodes.append(new_point)
            parents.append(nearest_index)
            new_cost = costs[nearest_index] + RRT._distance(
                nodes[nearest_index], new_point
            )
            costs.append(new_cost)
            new_index = len(nodes) - 1

            # Connect to the goal when it is reachable in one expansion and
            # the complete final edge also passes the collision check.
            if (RRT._distance(new_point, goal_point) <= step_size
                    and RRT._edge_is_free(occupancy_grid, new_point, goal_point)):
                nodes.append(goal_point)
                parents.append(new_index)
                costs.append(new_cost + RRT._distance(new_point, goal_point))
                goal_index = len(nodes) - 1
                # Trace parent indices from goal to start, then measure all edges.
                path = RRT._reconstruct_path(nodes, parents, goal_index)
                cost = sum(RRT._distance(a, b) for a, b in zip(path, path[1:]))
                RRT.last_cost_map = RRT._cost_map_from_tree(
                    occupancy_grid, nodes, costs
                )
                if verbose:
                    print(f"RRT reached the goal after {iteration} iterations.")
                    print(f"Path length: {cost:.2f} grid units")
                return path, cost

            if verbose and iteration % 250 == 0:
                print(f"RRT iteration {iteration}: {len(nodes)} nodes in the tree")

        # Save costs at every cell visited by the tree, even when no path
        # to the goal was found within the iteration limit.
        RRT.last_cost_map = RRT._cost_map_from_tree(
            occupancy_grid, nodes, costs
        )

        # Reaching this point means every allowed expansion was tried
        # without finding a safe connection to the goal.
        if verbose:
            print(f"RRT did not reach the goal in {max_iterations} iterations.")
        return None, math.inf

    # ==================================================
    # STEP 2: RECONSTRUCT THE FOUND PATH
    # ==================================================

    @staticmethod
    def _reconstruct_path(
        nodes: list[Point],
        parents: list[Optional[int]],
        goal_index: int
    ) -> list[Point]:
        """
        Follow parent pointers backward to reconstruct the path.

        The resulting chain is reversed before it is returned so the
        caller receives the points in Start -> Goal order.
        """
        path: list[Point] = []
        current: Optional[int] = goal_index
        while current is not None:
            path.append(nodes[current])
            current = parents[current]
        path.reverse()
        return path

    # ==================================================
    # STEP 3: VISUALIZE THE PLANNED PATH
    # ==================================================

    @staticmethod
    def visualize_path(
        occupancy_grid: np.ndarray,
        path: Optional[list[Point]],
        start: Cell,
        goal: Cell
    ) -> None:
        """
        Display obstacles, start, goal, tree costs and the RRT path.

        Each free cell shows the lowest accumulated tree cost g among RRT
        nodes in that cell. Free cells not visited by the tree show inf.
        Obstacles and unknown cells show X.
        """
        _visualize_path(
            occupancy_grid,
            path,
            start,
            goal,
            "RRT",
            "tab:blue",
            getattr(RRT, "last_cost_map", None)
        )


def _visualize_path(
    occupancy_grid: np.ndarray,
    path: Optional[list[Point]],
    start: Cell,
    goal: Cell,
    planner_name: str,
    path_color: str,
    cost_map: Optional[np.ndarray] = None
) -> None:
    """
    Draw obstacles, cell costs, start, goal and a planned path.

    RRT and RRT* use this shared display function with different path
    colors and titles. Path points are stored as (row, column), so the
    plot uses column for the horizontal axis and row for the vertical axis.
    """
    rows, cols = occupancy_grid.shape
    fig, ax = plt.subplots(figsize=(7, 7))
    # Convert free and occupied cells to a simple black-and-white image.
    ax.imshow((occupancy_grid != 0).astype(int), cmap="gray_r", vmin=0, vmax=1, origin="upper")
    ax.set_xticks(np.arange(-0.5, cols, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, rows, 1), minor=True)
    ax.grid(which="minor", color="gray", linewidth=0.8)

    # Draw the planned route when the search found one.
    if path:
        ax.plot(
            [point[1] for point in path],
            [point[0] for point in path],
            color=path_color,
            marker="o",
            linewidth=2.5,
            markersize=5,
            label=f"{planner_name} Path"
        )

    # Mark start and goal above the grid cell labels.
    ax.scatter(start[1], start[0], color="green", s=220, marker="s", label="Start", zorder=5)
    ax.scatter(goal[1], goal[0], color="red", s=220, marker="*", label="Goal", zorder=5)

    # Show the planner's cost at each free cell rather than its coordinates.
    for r in range(rows):
        for c in range(cols):
            if occupancy_grid[r, c] != 0:
                label, color = "X", "white"
            elif cost_map is None:
                label, color = "--", "black"
            elif np.isinf(cost_map[r, c]):
                label, color = "inf", "black"
            else:
                label, color = f"{cost_map[r, c]:.1f}", "black"
            ax.text(
                c, r, label,
                ha="center",
                va="center",
                fontsize=7,
                color=color,
                zorder=6
            )

    ax.set_title(f"{planner_name} Path Planning - Tree g Cost per Cell", fontsize=14)
    ax.set_xlabel("Grid Column")
    ax.set_ylabel("Grid Row")
    ax.set_xticks(np.arange(cols))
    ax.set_yticks(np.arange(rows))
    ax.legend(loc="upper right")
    plt.tight_layout()
    plt.show()
