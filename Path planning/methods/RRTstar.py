"""
========================================================================================
    Code for RRT* algorithm for mobile robot path planning
========================================================================================
    Author: Jogesh S Nanda
    Created: 10/10/2026
    Modified: 10/10/2026    (by Jogesh S Nanda)
========================================================================================
    Code created for class of MN207 (by Robotics Innovations Lab,
        Department of Design and Manufacturing, IISc).

    version : Python 3, NumPy, Matplotlib

Purpose:
    To plan, improve and visualize a low-cost collision-free path using RRT*
========================================================================================
"""

"""
RRT* ALGORITHM FOR MOBILE ROBOT PATH PLANNING
=============================================

Occupancy grid:
    0   = Free cell
    100 = Obstacle
    -1  = Unknown cell (treated as obstacle)

Outputs:
    1. Collision-free path from start to goal
    2. Total path length in grid units
    3. Graphical path visualization

RRT* improves the basic RRT tree by:
    1. Checking nearby nodes when choosing the new point's parent.
    2. Connecting through the least-cost safe parent.
    3. Rewiring nearby nodes when the new point gives a cheaper route.

The planner keeps growing the tree for the full iteration limit and then
returns the lowest-cost safe goal connection found in that tree.
"""

import math
from importlib import import_module
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np

# A position is represented as (row, column).
Point = tuple[float, float]
Cell = tuple[int, int]

# Reuse RRT's sampling, steering, collision checks and plot layout.
# RRT* changes how the tree selects parents and improves existing routes.
_rrt_module = import_module("methods.RRT")
_RRT = _rrt_module.RRT
_visualize_path = _rrt_module._visualize_path


# ==================================================
# STEP 1: RRT* PATH PLANNING
# ==================================================

class RRTStar(_RRT):
    """
    Plan and improve a collision-free path using RRT*.

    RRT* uses the same random sampling and collision checks as RRT. It
    also tracks the cost to each tree point so it can select a cheaper
    parent and rewire nearby branches when a better route is found.
    """

    @staticmethod
    def plan(
        occupancy_grid: np.ndarray,
        start: Cell,
        goal: Cell,
        max_iterations: int = 3000,
        step_size: float = 1.0,
        goal_sample_rate: float = 0.1,
        rewire_radius: float = 2.5,
        random_seed: Optional[int] = 0,
        verbose: bool = True
    ) -> tuple[Optional[list[Point]], float]:
        """
        Find a low-cost collision-free path using RRT*.

        Each valid sample extends the tree by at most step_size. Nearby
        nodes are considered as possible parents, and existing branches
        are rewired when the new point offers a shorter safe connection.
        After all iterations, the cheapest safe connection to the goal is
        returned.

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

        rewire_radius : float
            Maximum distance for considering nearby tree nodes. Larger
            values may improve parent choice but require more edge checks.

        random_seed : int or None
            Seed for repeatable random sampling. None uses a random seed.

        verbose : bool
            If True, print search progress.

        Returns
        -------
        path : list of (row, column) or None
            Lowest-cost collision-free path found.

        cost : float
            Total path length in grid units.
        """

        # ---------- Check the map and planner settings ----------
        if occupancy_grid.ndim != 2 or occupancy_grid.size == 0:
            raise ValueError("Occupancy grid must be a non-empty 2D array")
        if max_iterations <= 0 or step_size <= 0 or rewire_radius <= 0:
            raise ValueError("max_iterations, step_size and rewire_radius must be positive")
        if not 0.0 <= goal_sample_rate <= 1.0:
            raise ValueError("goal_sample_rate must be between 0 and 1")

        # ---------- Check that start and goal are valid free cells ----------
        rows, cols = occupancy_grid.shape
        for name, (r, c) in [("Start", start), ("Goal", goal)]:
            if not (0 <= r < rows and 0 <= c < cols):
                raise ValueError(f"{name} is outside the map")
            if occupancy_grid[r, c] != 0:
                raise ValueError(f"{name} is blocked")

        start_point: Point = (float(start[0]), float(start[1]))
        goal_point: Point = (float(goal[0]), float(goal[1]))
        if start == goal:
            RRTStar.last_cost_map = np.full(occupancy_grid.shape, math.inf, dtype=float)
            RRTStar.last_cost_map[start] = 0.0
            return [start_point], 0.0

        # ---------- Prepare the random sampler and search tree ----------
        # RRT supplies free-space sampling and the safe edge checker.
        free_cells = [
            (int(r), int(c))
            for r, c in np.argwhere(occupancy_grid == 0)
        ]
        if len(free_cells) < 2:
            return None, math.inf

        rng = np.random.default_rng(random_seed)
        # Each tree point has a parent index and a cumulative cost from start.
        # The start is the root, so its parent is None and its cost is zero.
        nodes: list[Point] = [start_point]
        parents: list[Optional[int]] = [None]
        costs = [0.0]

        # ==================================================
        # MAIN RRT* SEARCH LOOP
        # ==================================================
        for iteration in range(1, max_iterations + 1):
            # Occasionally sample the goal directly; otherwise choose a
            # random point from the free cells in the occupancy grid.
            if rng.random() < goal_sample_rate:
                sample = goal_point
            else:
                sample = _RRT._sample_free_point(occupancy_grid, free_cells, rng)

            # Find the nearest existing tree node and extend toward the sample.
            nearest_index = min(
                range(len(nodes)),
                key=lambda index: _RRT._distance(nodes[index], sample)
            )
            new_point = _RRT._steer(nodes[nearest_index], sample, step_size)

            # The new point itself must lie in a free cell before it can
            # be considered as part of the tree.
            if not _RRT._cell_is_free(occupancy_grid, new_point):
                continue

            # ---------- STEP A: FIND NEARBY TREE NODES ----------
            # Nearby nodes are possible parents and possible children to
            # rewire after this new point has been added.
            near_indices = [
                index for index, point in enumerate(nodes)
                if _RRT._distance(point, new_point) <= rewire_radius
            ]
            if nearest_index not in near_indices:
                near_indices.append(nearest_index)

            # ---------- STEP B: CHOOSE THE LEAST-COST PARENT ----------
            # The nearest node guarantees a basic RRT connection when safe.
            # Other nearby nodes may provide a cheaper route from the start.
            parent_candidates = [nearest_index] + [
                index for index in near_indices if index != nearest_index
            ]
            best_parent = None
            best_cost = math.inf
            for index in parent_candidates:
                edge_cost = _RRT._distance(nodes[index], new_point)
                candidate_cost = costs[index] + edge_cost
                if (candidate_cost < best_cost
                        and _RRT._edge_is_free(occupancy_grid, nodes[index], new_point)):
                    best_parent = index
                    best_cost = candidate_cost

            if best_parent is None:
                continue

            # Add the new point to the tree using the best safe parent found.
            nodes.append(new_point)
            parents.append(best_parent)
            costs.append(best_cost)
            new_index = len(nodes) - 1

            # ---------- STEP C: REWIRE NEARBY NODES ----------
            # Do not rewire the root or an ancestor of the new point: either
            # change would create a cycle in the parent links.
            ancestors = set()
            ancestor = best_parent
            while ancestor is not None:
                ancestors.add(ancestor)
                ancestor = parents[ancestor]

            for index in near_indices:
                if index == best_parent or index == 0 or index in ancestors:
                    continue

                candidate_cost = costs[new_index] + _RRT._distance(new_point, nodes[index])
                if (candidate_cost < costs[index]
                        and _RRT._edge_is_free(occupancy_grid, new_point, nodes[index])):
                    parents[index] = new_index
                    costs[index] = candidate_cost

                    # A changed parent cost also changes every descendant's
                    # cost. Build child links, then refresh that branch from
                    # the rewired point outward.
                    children: list[list[int]] = [[] for _ in nodes]
                    for child, parent in enumerate(parents):
                        if parent is not None:
                            children[parent].append(child)
                    pending = [index]
                    while pending:
                        current = pending.pop()
                        for child in children[current]:
                            costs[child] = costs[current] + _RRT._distance(
                                nodes[current], nodes[child]
                            )
                            pending.append(child)

            if verbose and iteration % 250 == 0:
                print(f"RRT* iteration {iteration}: {len(nodes)} nodes in the tree")

        # ==================================================
        # STEP 2: CONNECT THE GOAL TO THE LOWEST-COST TREE NODE
        # ==================================================
        # The goal is not inserted during the random loop. Check all tree
        # nodes now and keep only connections that are within one step and
        # collision-free along the complete edge.
        goal_candidates = [
            index for index, point in enumerate(nodes)
            if _RRT._distance(point, goal_point) <= step_size
            and _RRT._edge_is_free(occupancy_grid, point, goal_point)
        ]
        if not goal_candidates:
            RRTStar.last_cost_map = _RRT._cost_map_from_tree(
                occupancy_grid, nodes, costs
            )
            if verbose:
                print(f"RRT* did not reach the goal in {max_iterations} iterations.")
            return None, math.inf

        # Choose the reachable point with the smallest accumulated route
        # cost plus the final straight-line connection to the goal.
        best_goal_parent = min(
            goal_candidates,
            key=lambda index: costs[index] + _RRT._distance(nodes[index], goal_point)
        )
        # Reconstruct the tree route, then append the final goal connection.
        path = _RRT._reconstruct_path(nodes, parents, best_goal_parent)
        path.append(goal_point)
        total_cost = costs[best_goal_parent] + _RRT._distance(nodes[best_goal_parent], goal_point)
        RRTStar.last_cost_map = _RRT._cost_map_from_tree(
            occupancy_grid, nodes, costs
        )
        RRTStar.last_cost_map[goal] = total_cost

        if verbose:
            print(f"RRT* completed {max_iterations} iterations and found a path.")
            print(f"Path length: {total_cost:.2f} grid units")

        return path, total_cost

    # ==================================================
    # STEP 3: VISUALIZE THE IMPROVED PATH
    # ==================================================

    @staticmethod
    def visualize_path(
        occupancy_grid: np.ndarray,
        path: Optional[list[Point]],
        start: Cell,
        goal: Cell
    ) -> None:
        """
        Display obstacles, start, goal, tree costs and the RRT* path.

        Each free cell shows the lowest accumulated tree cost g among RRT*
        nodes in that cell. Free cells not visited by the tree show inf.
        Obstacles and unknown cells show X.
        """
        _visualize_path(
            occupancy_grid,
            path,
            start,
            goal,
            "RRT*",
            "tab:orange",
            getattr(RRTStar, "last_cost_map", None)
        )
