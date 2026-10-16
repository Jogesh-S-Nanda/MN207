# Lab Exercise 01: ROS 2 Python Nodes and Simulated Sensor Data

**Author:** Jogesh S Nanda, Robotics Innovation Lab (RIL), IISc  
**Purpose:** MN207 lab exercise  
**Copyright:** © Robotics Innovation Lab (RIL), IISc

## Objective

Create a ROS 2 workspace and Python package, write and run simple Python nodes,
and publish a simulated sensor reading. Record the commands and terminal
output as evidence of your work.

## Requirements

- A computer with ROS 2 installed and working (the course uses ROS 2 Jazzy).
- A terminal with the ROS 2 environment sourced.
- Python 3 and `colcon` available through the ROS 2 installation.

Use Bash commands below. Replace `YOUR_NAME`, `MEMBER_ONE`, and other example
names with your own details. Run commands in order, and resolve build or runtime
errors before continuing.

## 1. Create and enter a workspace

Create a workspace with a `src` directory, then enter its root:

```bash
mkdir -p ~/mn207_ws/src
cd ~/mn207_ws
```

Source ROS 2 in this terminal (adjust the distribution if your course setup
uses a different one):

```bash
source /opt/ros/jazzy/setup.bash
echo "$ROS_DISTRO"
```

The output should identify your installed ROS 2 distribution. Keep this terminal
open for the remaining steps.

## 2. Create a Python package

From the workspace root, create an `ament_python` package and inspect its files:

```bash
cd ~/mn207_ws/src
ros2 pkg create --build-type ament_python mn207_nodes
cd ~/mn207_ws
find src/mn207_nodes -maxdepth 3 -type f | sort
```

The package should contain `package.xml`, `setup.py`, a Python module directory,
and a `resource` marker. The nodes in this exercise belong in
`src/mn207_nodes/mn207_nodes/`.

## 3. Write a node that prints your name

Create `src/mn207_nodes/mn207_nodes/name_node.py` with the following content.
Replace the example name before saving:

```python
import rclpy
from rclpy.node import Node


class NameNode(Node):
    def __init__(self):
        super().__init__('name_node')
        self.get_logger().info('Hello, my name is YOUR_NAME')


def main(args=None):
    rclpy.init(args=args)
    node = NameNode()
    rclpy.spin_once(node, timeout_sec=0.1)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

Register it as a command-line executable. Open `src/mn207_nodes/setup.py` and
add this entry inside the existing `console_scripts` list, retaining any
existing entries:

```python
'name_node = mn207_nodes.name_node:main',
```

Build the package and source the workspace overlay:

```bash
cd ~/mn207_ws
colcon build --packages-select mn207_nodes
source install/setup.bash
ros2 run mn207_nodes name_node
```

Confirm that the terminal prints your name.

## 4. Write a class-based team counter node

Create `src/mn207_nodes/mn207_nodes/team_counter.py`. Change the team member
names in the list to the names of your team:

```python
import rclpy
from rclpy.node import Node


class TeamCounter(Node):
    def __init__(self):
        super().__init__('team_counter')
        self.members = ['MEMBER_ONE', 'MEMBER_TWO']
        self.count = 0
        self.timer = self.create_timer(1.0, self.print_team_status)

    def print_team_status(self):
        self.count += 1
        self.get_logger().info(
            f'Count: {self.count} | Team: {", ".join(self.members)}'
        )


def main(args=None):
    rclpy.init(args=args)
    node = TeamCounter()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

Add the following entry to the `console_scripts` list in `setup.py`:

```python
'team_counter = mn207_nodes.team_counter:main',
```

Rebuild and run the node:

```bash
cd ~/mn207_ws
colcon build --packages-select mn207_nodes
source install/setup.bash
ros2 run mn207_nodes team_counter
```

Observe that the count increases once per second and the team names are
displayed. Stop the node with <kbd>Ctrl</kbd>+<kbd>C</kbd>.

## 5. Simulate a sensor

Create `src/mn207_nodes/mn207_nodes/battery_sensor.py`. This node simulates a
battery voltage that decreases on each one-second timer callback and wraps back
to its starting value after reaching the lower limit:

```python
import rclpy
from rclpy.node import Node


class BatterySensor(Node):
    def __init__(self):
        super().__init__('battery_sensor')
        self.voltage = 12.6
        self.timer = self.create_timer(1.0, self.update_voltage)

    def update_voltage(self):
        self.voltage -= 0.1
        if self.voltage < 10.0:
            self.voltage = 12.6
        self.get_logger().info(f'Simulated battery voltage: {self.voltage:.1f} V')


def main(args=None):
    rclpy.init(args=args)
    node = BatterySensor()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

Register this executable in `setup.py`:

```python
'battery_sensor = mn207_nodes.battery_sensor:main',
```

Rebuild, source, and run it:

```bash
cd ~/mn207_ws
colcon build --packages-select mn207_nodes
source install/setup.bash
ros2 run mn207_nodes battery_sensor
```

Observe several readings, including the reset near 12.6 V, then stop with
<kbd>Ctrl</kbd>+<kbd>C</kbd>. This is simulated data logged by the node; it is
not a measurement from a physical battery.

## 6. Capture terminal commands and output

Append each node's terminal output (including errors) to `outdata.txt`. From
your workspace root, replace `<package>` and `<node>` with the package and
executable names, then run:

```bash
cd ~/mn207_ws
ros2 run <package> <node> 2>&1 | tee -a outdata.txt
```

For example, capture the name node with:

```bash
ros2 run mn207_nodes name_node 2>&1 | tee -a outdata.txt
```

Use the same pattern for `team_counter` and `battery_sensor`, and for each node
in the repeated package. For long-running nodes, capture a useful sample of
output and stop them with <kbd>Ctrl</kbd>+<kbd>C</kbd>. The `-a` option appends
each run to the same `outdata.txt` file. Also include a separate text file
listing the workspace, package creation, and build commands, since `tee`
captures the node command's output rather than a history of earlier commands.

## 7. Repeat the package and node work

Create a second Python package named `mn207_nodes_repeat` in the same
workspace. In it, repeat the package creation, name node, team counter, and
terminal capture steps. Use a different package name in the `ros2 pkg create`
command and in each executable's `setup.py` entry as appropriate. Update the
node names and log messages so your output clearly identifies the second
package. Build it with:

```bash
cd ~/mn207_ws
colcon build --packages-select mn207_nodes_repeat
source install/setup.bash
```

Run both executables from the repeated package and include their output in your
submission. You may also include the simulated sensor node from this package.

## Submission checklist

Submit one folder or archive containing:

1. `outdata.txt` with terminal output from the nodes in both rounds.
2. The complete `src/mn207_nodes/` and `src/mn207_nodes_repeat/` package
   directories, including the Python files and updated `setup.py` files.
3. A short `README.md` stating your name, team member names, ROS 2 distribution,
   commands used to build and run the nodes, and any issues you resolved.
4. A command list for workspace setup, package creation, and builds, plus
   evidence in `outdata.txt` that the name node ran, the team counter advanced at
   approximately 1 Hz, and the simulated voltage changed over time.

Before submitting, check that the package builds from a clean workspace and
that the executable names in `setup.py` match the `ros2 run` commands shown in
your logs. Do not include the workspace's generated `build/`, `install/`, or
`log/` directories unless your instructor specifically requests them.
