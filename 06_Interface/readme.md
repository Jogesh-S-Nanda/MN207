**Author:** Jogesh S Nanda, Robotics Innovation Lab (RIL), IISc  
**Purpose:** MN207 lab session — creating and testing custom ROS 2 interfaces  
**Copyright:** © Robotics Innovation Lab (RIL), IISc

# Custom ROS 2 Interfaces

This exercise uses a mobile robot example to show how to define, build, inspect, and use custom ROS 2 interfaces. The interface package is in `CustomDTs/` and its ROS package name is `custom_interfaces`.

| Interface | Example | Use |
|---|---|---|
| Message (`.msg`) | `RobotStatus` | A robot publishes a status snapshot. |
| Service (`.srv`) | `SetRobotMode` | A client requests a mode change and receives one response. |
| Action (`.action`) | `DriveDistance` | A client requests a longer movement, receives progress feedback, and gets a final result. |

## 1. Understand the interface definitions

Open the files under `CustomDTs/msg`, `CustomDTs/srv`, and `CustomDTs/action`.

- A message lists fields, one per line. Field names use lowercase `snake_case`.
- A service separates its request fields from its response fields with one `---` line.
- An action separates its goal, result, and feedback fields with two `---` lines.
- Each field is a type followed by a field name. ROS 2 supports primitive types such as `bool`, `int32`, `float32`, and `string`, as well as arrays and fields from other interface packages.
- `RobotStatus` uses `geometry_msgs/Pose2D` and `geometry_msgs/Twist`, so the package must declare its dependency on `geometry_msgs`.

For example, the `DriveDistance.action` goal contains `distance_m` and `speed_mps`. Its result describes completion, and its feedback describes motion progress. An action definition describes the data exchanged; it does not implement a robot controller or action server.

## 2. Create a ROS 2 workspace

The commands below use ROS 2 Jazzy on Ubuntu. Open a terminal and source the Jazzy environment:

```bash
source /opt/ros/jazzy/setup.bash
mkdir -p ~/mn207_ws/src
```

Copy the `CustomDTs` directory from this course repository into `~/mn207_ws/src/CustomDTs`. The workspace should then look like this:

```text
mn207_ws/
└── src/
    └── CustomDTs/
        ├── CMakeLists.txt
        ├── package.xml
        ├── action/
        ├── msg/
        └── srv/
```

The folder name may be `CustomDTs`; the package name used by ROS 2 is `custom_interfaces`, as specified in `package.xml` and `CMakeLists.txt`.

## 3. Define or edit an interface

Create each definition under the folder for its interface kind:

```text
CustomDTs/msg/YourMessage.msg
CustomDTs/srv/YourService.srv
CustomDTs/action/YourAction.action
```

Use one field per line. In a service, place `---` between request and response. In an action, place one `---` after the goal and another after the result. If a definition uses a type from another ROS package, add that dependency to both `package.xml` and the `rosidl_generate_interfaces(... DEPENDENCIES ...)` section of `CMakeLists.txt`.

The current package registers its three examples in `CMakeLists.txt`:

```cmake
rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/RobotStatus.msg"
  "srv/SetRobotMode.srv"
  "action/DriveDistance.action"
  DEPENDENCIES geometry_msgs
)
```

When adding a file, add its path to this list. Keep the package name in `CMakeLists.txt` consistent with the `<name>` in `package.xml`.

## 4. Build and source the interface package

Install dependencies declared in the package manifest, build the package, and source the workspace overlay:

```bash
cd ~/mn207_ws
rosdep install --from-paths src --ignore-src -r -y
colcon build --packages-up-to custom_interfaces
source install/setup.bash
```

Source both `/opt/ros/jazzy/setup.bash` and `install/setup.bash` in every new terminal where you want to use the generated interfaces. Rebuild and source the workspace again after changing an interface definition.

## 5. Inspect the generated interfaces

These commands confirm that ROS 2 can find the package and show the generated type definitions:

```bash
ros2 interface package custom_interfaces
ros2 interface list
ros2 interface show custom_interfaces/msg/RobotStatus
ros2 interface show custom_interfaces/srv/SetRobotMode
ros2 interface show custom_interfaces/action/DriveDistance
```

`ros2 interface list` lists interfaces from all sourced packages. To narrow the output, pipe it through `grep custom_interfaces` on Ubuntu:

```bash
ros2 interface list | grep custom_interfaces
```

## 6. Test and inspect a message topic

The interface package defines a message type, but it does not create a publisher or topic by itself. To test the message with the ROS 2 CLI, publish a sample status repeatedly in one terminal:

```bash
ros2 topic pub --rate 1 /robot/status custom_interfaces/msg/RobotStatus \
  "{robot_name: rover_1, is_moving: false, battery_percent: 87.5, pose: {x: 1.0, y: 2.0, theta: 0.5}, velocity: {linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}}"
```

In a second sourced terminal, use these commands to inspect the topic and see its messages:

```bash
ros2 topic list -t
ros2 topic type /robot/status
ros2 topic info /robot/status --verbose
ros2 topic echo /robot/status
```

Stop the publisher with `Ctrl+C`. `ros2 topic pub` is useful for testing the message shape and a subscriber; it does not test a robot-specific publisher implementation.

## 7. Test and inspect a service

A service definition alone does not provide a service server. Start a node that creates a server using `custom_interfaces/srv/SetRobotMode` before making a call. Then, from another sourced terminal, list and inspect the running service:

```bash
ros2 service list -t
ros2 service type /set_robot_mode
ros2 service find custom_interfaces/srv/SetRobotMode
ros2 service info /set_robot_mode
```

Call it with the request fields. This example requests mode `1`; the meaning of each mode value must be agreed on by the server and client:

```bash
ros2 service call /set_robot_mode custom_interfaces/srv/SetRobotMode "{mode: 1}"
```

The call succeeds only when a compatible server is running and the service name matches. A timeout or “service not available” message usually means the server is not running, the name differs, or the terminals have different ROS domain settings.

## 8. Test and inspect an action

An action definition alone does not provide an action server. Start a node that creates an action server using `custom_interfaces/action/DriveDistance` at `/drive_distance`. The example client in `05_Actions/Client.py` is a client only; it also needs a matching server to accept its goal.

Inspect the running action and send a sample goal with feedback enabled:

```bash
ros2 action list -t
ros2 action info /drive_distance
ros2 action send_goal /drive_distance custom_interfaces/action/DriveDistance \
  "{distance_m: 1.0, speed_mps: 0.2}" --feedback
```

The server should accept the goal, publish `distance_travelled_m` and `remaining_distance_m` feedback, then return a result. If the action is unavailable, check that its server is running and that the action name and type match.

## ROS 2 Jazzy interface and diagnostics command reference

| Command | Purpose |
|---|---|
| `ros2 interface list` | List visible message, service, and action types. |
| `ros2 interface package <package>` | List interfaces belonging to a package. |
| `ros2 interface show <package>/<kind>/<Type>` | Print a message, service, or action definition. |
| `ros2 topic list -t` | List topics and their types. |
| `ros2 topic type <topic>` | Show the type on one topic. |
| `ros2 topic info <topic> --verbose` | Inspect topic type, publishers, subscribers, and QoS details. |
| `ros2 topic echo <topic>` | Display messages received from a topic. |
| `ros2 topic pub --rate 1 <topic> <type> '<values>'` | Publish a sample message repeatedly. |
| `ros2 service list -t` | List active services and their types. |
| `ros2 service type <service>` | Show the type of one active service. |
| `ros2 service find <type>` | Find active services of a given type. |
| `ros2 service info <service>` | Inspect the server node and service type. |
| `ros2 service call <service> <type> '<request>'` | Send a request to a running service. |
| `ros2 action list -t` | List active actions and their types. |
| `ros2 action info <action>` | Inspect the action server and clients. |
| `ros2 action send_goal <action> <type> '<goal>' --feedback` | Send a goal and print feedback from a running server. |
| `ros2 node list` | List active ROS nodes. |
| `ros2 node info <node>` | Inspect a node's topics, services, and actions. |
| `ros2 doctor --report` | Print a ROS environment and graph diagnostic report. |

Replace `<topic>`, `<service>`, `<action>`, `<type>`, and `<values>` with the names shown in the examples. Topic, service, and action graph commands report active endpoints; they do not report definitions that are merely present in source files.

## Troubleshooting checklist

1. Confirm the ROS distribution and environment: `echo "$ROS_DISTRO"` should print `jazzy`.
2. Source `/opt/ros/jazzy/setup.bash`, then source `~/mn207_ws/install/setup.bash` in the current terminal.
3. Confirm `custom_interfaces` appears in `ros2 interface package custom_interfaces` and that the expected types appear in `ros2 interface list`.
4. If a new type is missing, rebuild from the workspace root with `colcon build --packages-up-to custom_interfaces`, then source `install/setup.bash` again.
5. If the build reports a missing dependency, run `rosdep install --from-paths src --ignore-src -r -y` from the workspace root.
6. If a topic, service, or action is missing, make sure the node that creates that endpoint is running. Definitions do not launch nodes.
7. If endpoints are visible in one terminal but not another, source the same workspace in both and check `ROS_DOMAIN_ID` and `RMW_IMPLEMENTATION`.

For more details, see the [ROS 2 Jazzy interface tutorial](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Interfaces/Understanding-ROS2-Interfaces.html), [colcon build tutorial](https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Colcon-Tutorial.html), and [ROS 2 CLI tools](https://docs.ros.org/en/jazzy/How-To-Guides/Using-ros2doctor.html).
