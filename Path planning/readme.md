# Mobile Robot Path Planning

Educational examples for learning and comparing four path-planning algorithms on 2D occupancy grids. Each example defines its own map, start, goal, and cell resolution, then calls the reusable planner classes in `methods`.

**Author:** Jogesh S Nanda, Robotics Innovation Lab (RIL), IISc  
**Purpose:** MN207 lab session  
**Copyright:** © Robotics Innovation Lab (RIL), IISc

## Folder contents

```text
Path planning/
â”œâ”€â”€ methods/
â”‚   â”œâ”€â”€ dijistra.py   # Dijkstra's algorithm
â”‚   â”œâ”€â”€ Astar.py      # A* search
â”‚   â”œâ”€â”€ RRT.py        # Rapidly-exploring Random Tree
â”‚   â””â”€â”€ RRTstar.py    # RRT* with parent selection and rewiring
â”œâ”€â”€ Example 01.py    # Small map for getting started
â”œâ”€â”€ Example 02.py    # Medium map with more obstacles
â”œâ”€â”€ Example 03.py    # Larger map for comparing the planners
â””â”€â”€ readme.md
```

The files in `methods` contain reusable planner classes. The examples contain the maps and show how to call each planner. This keeps map design separate from the algorithm implementation, so you can try new maps without editing the planners.

## Algorithms

### Dijkstra

Dijkstra expands the reachable cell with the lowest known cost from the start. It finds an optimal path on this grid when a path exists. Each horizontal or vertical move costs one grid step. The plot labels each free cell with `g`, its lowest known cost from the start.

### A*

A* orders its search using:

```text
f = g + h
```

`g` is the known cost from the start, and `h` estimates the remaining cost to the goal. These examples use Manhattan distance for `h`, which matches four-connected movement with unit step costs. The plot labels cells with `f`.

### RRT

RRT grows a tree from the start. It samples free locations, extends the nearest tree point toward a sample, and checks the full edge for collisions before adding it. The first safe connection to the goal is returned. Since the search is randomized, a run may not find a path within its iteration limit. The plot shows accumulated tree cost `g` for visited cells; cells the tree did not visit show `inf`.

### RRT*

RRT* extends RRT by checking nearby tree points for a lower-cost parent and rewiring branches when a cheaper safe route is found. It keeps searching for the full iteration limit and returns the lowest-cost goal connection it found. As with RRT, the finite run is randomized and does not guarantee a globally optimal path. Its plot shows accumulated tree cost `g` for visited cells; unvisited cells show `inf`.

## Grid and coordinate conventions

Each example defines a NumPy array named `grid`:

| Value | Meaning |
| --- | --- |
| `0` | Free cell; the robot can enter it. |
| `100` | Obstacle; the robot must avoid it. |
| `-1` | Unknown cell; treated as blocked. |

Any nonzero cell is treated as blocked by the planners. Positions are written as `(row, column)`: row increases downward and column increases to the right. For example, `(0, 0)` is the top-left cell. The plot's horizontal axis is column and its vertical axis is row.

`resolution` gives the physical width or height of one square cell in meters. Dijkstra and A* return costs in grid steps; RRT and RRT* return Euclidean path lengths in grid units. Multiply a returned cost by `resolution` to estimate path length in meters, as the examples do.

In the plots, green squares mark the start, red stars mark the goal, and `X` marks blocked cells. Numeric cell labels show the algorithm's cost function. For A*, that value is `f = g + h`; for the other planners it is cost-to-come `g`.

## Requirements and running an example

The examples use Python 3, NumPy, and Matplotlib. They do not require a ROS installation; they plan over the occupancy grid in Python.

Install the packages into the Python environment configured for this project if needed:

```powershell
python -m pip install numpy matplotlib
```

From the `Path planning` folder, run one example:

```powershell
python ".\Example 01.py"
```

You can also open an example in PyCharm and run the file. Each example runs Dijkstra, A*, RRT, and RRT* in order. Each successful planner opens a separate plot; close the current plot window to continue to the next result. The grid-based planners print their search matrices when `verbose=True`.

## Make your own example

The simplest way to experiment is to copy one of the example files, give it a new name such as `Example 04.py`, and change the map inputs. Keep the planners in `methods` unchanged while you explore different maps.

1. Create a rectangular NumPy array. Use `0` for free cells and nonzero values for obstacles or unknown cells.
2. Choose `start` and `goal` as `(row, column)` positions. Check that both positions are within the map and contain `0`.
3. Set `resolution` to the physical cell size in meters.
4. Keep or adjust each planner call. RRT and RRT* accept `max_iterations`, `step_size`, `goal_sample_rate`, and `random_seed`. RRT* also accepts `rewire_radius`.
5. Run the example and compare the paths, cost labels, printed costs, and search behavior.

For repeatable RRT results, keep `random_seed` fixed. Change the seed to see how random samples affect the tree and the returned path. Increasing `max_iterations` gives RRT and RRT* more opportunities to find or improve a route, at the cost of longer runtime.

## Calling a planner directly

The examples load the reusable classes from `methods`. For example:

```python
from importlib import import_module

Dijkstra = import_module("methods.dijistra").Dijkstra
path, cost = Dijkstra.plan(grid, start, goal, verbose=True)

if path is not None:
    Dijkstra.visualize_path(grid, path, start, goal)
```

The other classes are `AStar` from `methods.Astar`, `RRT` from `methods.RRT`, and `RRTStar` from `methods.RRTstar`. Each `plan()` method returns `(path, cost)`. When no path is found, `path` is `None` and `cost` is infinity. A planner raises `ValueError` when a start or goal is outside the map or blocked.

## Learning suggestions

- Start with Example 01 and trace the printed Dijkstra distance, visited, and parent matrices.
- Compare Dijkstra and A* on the same map. Notice how the heuristic guides A* toward the goal while preserving the shortest path for this movement model.
- Change a few obstacle cells and observe how the cost field and route change.
- Compare RRT and RRT* with the same random seed. Inspect how RRT* uses nearby nodes to lower the tree cost.
- Try a blocked route or a narrow passage. Observe that sampling-based planners may need more iterations or a different seed.
