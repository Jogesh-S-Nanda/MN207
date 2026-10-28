# Lab Exercise 02: ROS 2 Publisher, Subscriber, and Remapping

**Author:** Jogesh S Nanda, Robotics Innovation Lab (RIL), IISc  
**Purpose:** MN207 lab exercise  
**Copyright:** © Robotics Innovation Lab (RIL), IISc

## Objective

Publish simulated temperature readings to a ROS 2 topic from the terminal,
subscribe to those readings from another terminal, and use ROS 2 remapping to
change the node names and topic name. Record the commands and terminal output
as evidence of your work.

## Requirements

- A computer with ROS 2 installed and working (the course uses ROS 2 Jazzy).
- Two terminals with the ROS 2 environment sourced.
- The same ROS domain ID in both terminals (use the default unless instructed
  otherwise).

Use Bash commands below. Replace example names with your own where appropriate.
Run the terminals simultaneously: keep the subscriber running while you start
the publisher.

## 1. Prepare both terminals

In **Terminal 1** and **Terminal 2**, source ROS 2 (adjust the distribution if
your course setup uses a different one):

```bash
source /opt/ros/jazzy/setup.bash
echo "$ROS_DISTRO"
```

The output should identify your installed ROS 2 distribution.

## 2. Publish simulated sensor data

In **Terminal 1**, publish a changing sequence of simulated temperature
readings as `std_msgs/msg/String` messages on the `/sensor` topic. The
`'{data: ...}'` value is the message content; `-r 2` publishes it twice per
second:

```bash
ros2 topic pub -r 2 /sensor std_msgs/msg/String "{data: 'Simulated temperature: 22.5 C'}"
```

Leave this command running. It repeatedly publishes the sample reading. This
is demonstration data, not a measurement from a physical sensor.

## 3. Subscribe and inspect the topic

In **Terminal 2**, display each message received on `/sensor`:

```bash
ros2 topic echo /sensor
```

Confirm that the simulated temperature appears repeatedly. You can also inspect
the topic type and publisher/subscriber connections in another terminal:

```bash
ros2 topic type /sensor
ros2 topic info /sensor --verbose
```

The topic type should be `std_msgs/msg/String`. Stop the echo and publisher
with <kbd>Ctrl</kbd>+<kbd>C</kbd> when you are ready to continue.

## 4. Rename the topic from the terminal

ROS 2 remapping changes the topic name seen by a node without editing its
source. In **Terminal 1**, publish the same simulated data on `/temperature`
instead of `/sensor`:

```bash
ros2 topic pub -r 2 /temperature std_msgs/msg/String "{data: 'Simulated temperature: 22.5 C'}"
```

In **Terminal 2**, subscribe to the renamed topic:

```bash
ros2 topic echo /temperature
```

Verify that messages arrive on `/temperature`. A subscriber still listening
to `/sensor` will not receive these messages; publisher and subscriber topic
names must match. Stop both commands with <kbd>Ctrl</kbd>+<kbd>C</kbd>.

## 5. Remap node and topic names at launch

The ROS 2 `topic pub` and `topic echo` commands create temporary ROS nodes.
The `--ros-args` options below assign those nodes explicit names and remap
`/sensor` to `/temperature` for each command.

In **Terminal 1**, run the publisher with a node name and topic remap:

```bash
ros2 topic pub -r 2 /sensor std_msgs/msg/String "{data: 'Simulated temperature: 22.5 C'}" --ros-args -r __node:=temperature_publisher -r /sensor:=/temperature
```

In **Terminal 2**, run the subscriber with its own node name and the matching
topic remap:

```bash
ros2 topic echo /sensor --ros-args -r __node:=temperature_subscriber -r /sensor:=/temperature
```

Confirm that the subscriber receives messages. In a third terminal, inspect
the active nodes and renamed topic:

```bash
ros2 node list
ros2 topic list
ros2 topic info /temperature --verbose
```

The node list should include `temperature_publisher` and
`temperature_subscriber`, and the topic list should include `/temperature`.
Depending on the ROS 2 distribution, the `ros2 topic` command may create
additional helper nodes as well. Stop the publisher and subscriber with
<kbd>Ctrl</kbd>+<kbd>C</kbd>.

## 6. Save your terminal evidence

Capture the commands and a useful sample of their output in `outdata.txt`. For
example, run each command with `tee` in its terminal:

```bash
ros2 topic pub -r 2 /sensor std_msgs/msg/String "{data: 'Simulated temperature: 22.5 C'}" 2>&1 | tee -a outdata.txt
```

```bash
ros2 topic echo /sensor 2>&1 | tee -a outdata.txt
```

Use the same pattern for the remapped commands. The `-a` option appends output
to the file. Also save a short command list containing the ROS 2 sourcing,
publish, echo, and remapping commands, since `tee` only captures the command
to which it is attached and its output.

## Submission checklist

Submit one folder or archive containing:

1. `outdata.txt` with publisher and subscriber output, including evidence of
   the renamed node and topic names.
2. A short `README.md` stating your name, ROS 2 distribution, commands used,
   and any issues you resolved.
3. A command list for sourcing ROS 2, publishing and echoing the simulated
   sensor data, and applying the node and topic remaps.

Before submitting, check that the subscriber received messages in both the
original and remapped examples, and that the publisher and subscriber used the
same topic name in each example.
