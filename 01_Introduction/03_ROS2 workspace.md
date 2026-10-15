# 04. Create and Inspect a ROS 2 Workspace

**Author:** Jogesh S Nanda, Robotics Innovation Lab (RIL), IISc  
**Purpose:** MN207 lab session  
**Copyright:** © Robotics Innovation Lab (RIL), IISc


In this exercise, create a workspace named `workspace01` in your Documents
folder. Add one minimal Python package and one minimal C++ package, build them
with `colcon`, and use ROS 2 commands to inspect the result.

> Bash terminal. Run each command in order. A workspace is a directory that
> contains packages under `src/`; build commands are run from the workspace
> root, not from `src/`.

## 1. Open a terminal and source ROS 2

Open a terminal with <kbd>Ctrl</kbd> + <kbd>Alt</kbd> + <kbd>T</kbd>. Source
the Jazzy environment in this terminal:

```bash
source /opt/ros/jazzy/setup.bash
```

Check that the environment is available:

```bash
printenv ROS_DISTRO
ros2 --help
```

`printenv ROS_DISTRO` should print `jazzy`. If `ros2` is not found, check the
installation guide and source command before continuing.

## 2. Create the workspace folders

Create `workspace01` inside Documents, with an initially empty `src` folder:

```bash
mkdir -p ~/Documents/workspace01/src
cd ~/Documents/workspace01
```

Confirm your current location and inspect the folders:

```bash
pwd
ls -la
ls -la src
```

`pwd` should end with `/Documents/workspace01`. The `src` folder should be
empty at this point. The `build`, `install`, and `log` folders will be created
by the first build.

## 3. Create a minimal Python package

From the workspace root, create a package named `empty_py_pkg`:

```bash
cd ~/Documents/workspace01/src
ros2 pkg create empty_py_pkg --build-type ament_python
```

Inspect the package files:

```bash
cd ~/Documents/workspace01
find src/empty_py_pkg -maxdepth 2 -type f | sort
```

The package contains the metadata and setup files needed for a Python ROS 2
package. It has no node yet.

## 4. Create a minimal C++ package

Create a second package named `empty_cpp_pkg`:

```bash
cd ~/Documents/workspace01/src
ros2 pkg create empty_cpp_pkg --build-type ament_cmake
```

Inspect its files:

```bash
cd ~/Documents/workspace01
find src/empty_cpp_pkg -maxdepth 2 -type f | sort
```

This package has the CMake metadata for a C++ ROS 2 package. It does not yet
contain a node or executable.

## 5. Build both packages with colcon

Build from the workspace root:

```bash
cd ~/Documents/workspace01
colcon build
```

Wait for the build to finish. A successful build ends with a summary showing
both packages as finished. `colcon` creates `build/`, `install/`, and `log/`.

Source the workspace overlay in this terminal so ROS 2 can find these packages:

```bash
source install/setup.bash
```

An overlay adds this workspace's packages to the ROS environment on top of the
underlying Jazzy installation. Source it again in each new terminal where you
want to use this workspace.

## 6. Inspect the workspace and packages

Run these commands from `~/Documents/workspace01`:

```bash
colcon list
ros2 pkg list | sort | grep -E '^empty_(py|cpp)_pkg$'
ros2 pkg prefix empty_py_pkg
ros2 pkg prefix empty_cpp_pkg
```

Check that `colcon list` shows both packages and their build types. The package
list filter should print both names. Each `ros2 pkg prefix` command should
print a path under `~/Documents/workspace01/install`.

## 7. Try ROS 2 diagnostics

These commands help inspect the current ROS environment and running ROS graph.
Some graph commands will show little or no data until a node is running; that
is expected because the two packages are currently empty.

```bash
ros2 doctor --report
ros2 node list
ros2 topic list
ros2 service list
ros2 interface list | head
```

`ros2 doctor --report` reports environment and system checks. The node, topic,
and service lists describe active ROS graph entities; with no running nodes,
they may be empty (or include only built-in entries).

To compare with a live graph, open a **second terminal**, then run:

```bash
source /opt/ros/jazzy/setup.bash
ros2 run demo_nodes_cpp talker
```

Keep the talker running. In the first terminal, source the workspace again if
needed and inspect the graph:

```bash
source /opt/ros/jazzy/setup.bash
source ~/Documents/workspace01/install/setup.bash
ros2 node list
ros2 topic list
ros2 topic info /chatter
ros2 topic type /chatter
ros2 topic echo --once /chatter
```

You should see a talker node and the `/chatter` topic. The topic type should be
`std_msgs/msg/String`, and `echo --once` should display one message. Stop the
talker with <kbd>Ctrl</kbd> + <kbd>C</kbd> in its terminal. Then run
`ros2 node list` again and observe the change.

## 8. Check build output and logs

Return to the workspace root and inspect build results:

```bash
cd ~/Documents/workspace01
colcon list
ls
ls log/latest_build
```

If the build fails, read the terminal error first. Then inspect the latest
build log:

```bash
find log/latest_build -maxdepth 3 -type f | sort
```

Correct the reported issue and rebuild. To build only one package after a
change, use:

```bash
colcon build --packages-select empty_py_pkg
```

The Python package name can be selected here even though no Python node has
been added.

## 9. Common problems

| Symptom | Check |
|---|---|
| `ros2: command not found` | Run `source /opt/ros/jazzy/setup.bash` and check `printenv ROS_DISTRO`. |
| `colcon: command not found` | Confirm the ROS development tools are installed. |
| Package is not found by `ros2 pkg` | Build from the workspace root, then source `install/setup.bash` in the same terminal. |
| `colcon build` cannot find a package | Check that the package is inside `workspace01/src/` and that the command is being run from `workspace01/`. |
| No nodes or topics appear | This is normal when no ROS nodes are running. Start the demo talker to inspect a live graph. |
| Build failed | Read the first relevant error in the terminal and inspect files under `log/latest_build/`. |

## Student checksheet

Check each item when you have completed it. Be ready to show the workspace and
describe what each diagnostic command tells you.

- [ ] I sourced `/opt/ros/jazzy/setup.bash` and confirmed `ROS_DISTRO` is `jazzy`.
- [ ] I created `~/Documents/workspace01/src` and verified the workspace path.
- [ ] I created `empty_py_pkg` with the `ament_python` build type.
- [ ] I created `empty_cpp_pkg` with the `ament_cmake` build type.
- [ ] I ran `colcon build` from the workspace root and it completed successfully.
- [ ] I sourced `install/setup.bash` and found both packages with `ros2 pkg`.
- [ ] I ran `colcon list` and `ros2 doctor --report`.
- [ ] I inspected node, topic, and service lists with no nodes running.
- [ ] I started the demo talker and inspected `/chatter` with `ros2 topic info`, `ros2 topic type`, and `ros2 topic echo --once`.
- [ ] I stopped the talker and observed the ROS graph update.
- [ ] I can locate the latest build logs under `log/`.
