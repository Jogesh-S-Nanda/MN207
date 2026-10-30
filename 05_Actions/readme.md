**Author:** Jogesh S Nanda, Robotics Innovation Lab (RIL), IISc  
**Purpose:** MN207 lab session — ROS 2 action server and client  
**Copyright:** © Robotics Innovation Lab (RIL), IISc

# ROS 2 Actions

This exercise uses a mobile robot example to demonstrate an action server and client. The client requests that the robot drive a distance at a selected speed. The server reports progress while the goal is running and returns a result when the simulated drive finishes.

Actions suit tasks that take time and need feedback while they run. The action definition specifies the goal, result, and feedback fields; the server code implements the behavior.

## Files in this directory

| File | What it demonstrates |
|---|---|
| `Server.py` | A simulated mobile robot action server at `/drive_distance`. |
| `Client.py` | An action client that sends a goal, receives feedback, and prints the result. |

The action type is `custom_interfaces/action/DriveDistance`, defined in `06_Interface/CustomDTs/action/DriveDistance.action`.

## 1. Prepare the ROS 2 environment

These commands use ROS 2 Jazzy on Ubuntu. In each terminal, source ROS 2 and the workspace overlay where `custom_interfaces` was built:

```bash
source /opt/ros/jazzy/setup.bash
source ~/mn207_ws/install/setup.bash
```

If you have not built the interface package yet, follow the workspace and build steps in [`06_Interface/readme.md`](../06_Interface/readme.md). Confirm the generated action type is available:

```bash
ros2 interface show custom_interfaces/action/DriveDistance
```

The goal fields are `distance_m` and `speed_mps`. The result fields are `success`, `distance_travelled_m`, and `message`. The feedback fields are `distance_travelled_m` and `remaining_distance_m`.

## 2. Understand the action definition

`DriveDistance.action` has three sections separated by `---` lines:

```text
float32 distance_m
float32 speed_mps
---
bool success
float32 distance_travelled_m
string message
---
float32 distance_travelled_m
float32 remaining_distance_m
```

The first section is the goal sent by the client. The second section is the final result returned by the server. The third section is feedback published while the goal is executing.

## 3. Create the action server

Open `Server.py` and follow the server structure:

1. Import `rclpy`, `Node`, `ActionServer`, `GoalResponse`, and the generated `DriveDistance` action type.
2. Define a node class and create an `ActionServer` using the `DriveDistance` type and the name `drive_distance`.
3. In the goal callback, accept positive distance and speed values and reject invalid goals.
4. In the execute callback, read the goal fields and simulate motion over time.
5. Create and publish a feedback message on each update.
6. Mark the goal as succeeded, fill in the result fields, and return the result.
7. In `main()`, initialize ROS and spin the server node so it can receive goals.

The server simulates movement; it does not publish velocity commands or control a physical robot. Its update interval is `0.2` seconds, so the client goal of 1 metre at 0.2 metres per second takes about 5 seconds.

Run the server from the `05_Actions` directory in **Terminal 1**:

```bash
python3 Server.py
```

Keep this terminal running while sending goals. The server should report that `/drive_distance` is ready.

## 4. Create and run the action client

Open `Client.py` and follow the client structure:

1. Create an `ActionClient` using the same `DriveDistance` type and action name, `drive_distance`.
2. Wait for the action server with `wait_for_server()`.
3. Create a `DriveDistance.Goal` and set its `distance_m` and `speed_mps` fields.
4. Send the goal asynchronously and register callbacks for the goal response, feedback, and result.
5. In the feedback callback, display the travelled and remaining distances.
6. In the result callback, display whether the drive succeeded, how far it travelled, and the server message.

In **Terminal 2**, source the same ROS environments and run the client:

```bash
source /opt/ros/jazzy/setup.bash
source ~/mn207_ws/install/setup.bash
cd /path/to/MN207/05_Actions
python3 Client.py
```

Replace `/path/to/MN207` with the location of this course repository. The client sends a 1 metre goal at 0.2 metres per second. Expected output includes `Goal accepted`, repeated progress feedback, and a final result with `success=True` and `Target distance reached`.

## 5. Inspect and test the action using ROS 2 commands

With `Server.py` running, use another sourced terminal to inspect the action server and its node:

```bash
ros2 action list -t
ros2 action info /drive_distance
ros2 node list
ros2 node info /drive_distance_server
```

Send a goal directly from the ROS 2 command line. The `--feedback` option prints progress as it arrives:

```bash
ros2 action send_goal /drive_distance custom_interfaces/action/DriveDistance \
  "{distance_m: 1.0, speed_mps: 0.2}" --feedback
```

Try other positive values, for example a shorter goal or a higher speed:

```bash
ros2 action send_goal /drive_distance custom_interfaces/action/DriveDistance \
  "{distance_m: 0.5, speed_mps: 0.5}" --feedback
```

Try an invalid goal to see the server reject it:

```bash
ros2 action send_goal /drive_distance custom_interfaces/action/DriveDistance \
  "{distance_m: 0.0, speed_mps: 0.2}" --feedback
```

## ROS 2 Jazzy action command reference

| Command | Purpose |
|---|---|
| `ros2 action list` | List active action names. |
| `ros2 action list -t` | List active actions and their types. |
| `ros2 action info <action>` | Inspect the action type and connected servers and clients. |
| `ros2 action send_goal <action> <type> '<goal>' --feedback` | Send a goal and display feedback and the result. |
| `ros2 interface show <package>/action/<Type>` | Display the goal, result, and feedback fields. |
| `ros2 node list` | List active ROS nodes. |
| `ros2 node info <node>` | Inspect a node's actions and other graph connections. |
| `ros2 doctor --report` | Print information that can help diagnose the ROS environment. |
| `ros2 --help` | List available ROS 2 command groups. |

Replace angle bracket values with the action name, type, or node name. The action server must be running for action discovery and goal commands to work.

## Troubleshooting

1. If `custom_interfaces.action` cannot be imported, build `custom_interfaces` and source the workspace overlay in the current terminal.
2. If the client waits for the server, check that `Server.py` is running and both programs use `/drive_distance` with `custom_interfaces/action/DriveDistance`.
3. If the goal is rejected, check that both `distance_m` and `speed_mps` are greater than zero.
4. If feedback or results are missing, check the server terminal for errors and confirm that the client and server use matching goal, feedback, and result fields.
5. If terminals cannot discover each other, source the same ROS environment and check that their `ROS_DOMAIN_ID` values match.
6. Stop a running node with `Ctrl+C`.

For more detail, see the [ROS 2 Jazzy actions tutorial](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Actions/Understanding-ROS2-Actions.html), the [action server and client tutorial](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Writing-an-Action-Server-Client/Py.html), and the [ROS 2 CLI tools guide](https://docs.ros.org/en/jazzy/Concepts/Basic/About-Command-Line-Tools.html).
