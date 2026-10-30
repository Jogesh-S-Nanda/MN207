**Author:** Jogesh S Nanda, Robotics Innovation Lab (RIL), IISc  
**Purpose:** MN207 lab session — ROS 2 service server and client  
**Copyright:** © Robotics Innovation Lab (RIL), IISc

# ROS 2 Services

This exercise walks through the service server and client examples in this directory. The server adds two integers and returns their sum using the standard `example_interfaces/srv/AddTwoInts` service type.

A service uses a request/response pattern: a client sends a request, the server processes it, and the server returns a response. Start the server before running a client.

## Files in this directory

| File | What it demonstrates |
|---|---|
| `Server.py` | A class based service server. It provides `/add_two_ints`. |
| `Client.py` | A simple client that creates a `Node` directly, sends one request, and waits for its response. |
| `Client Oop.py` | A class based client with methods for waiting for the server, sending requests, and handling responses. |

## 1. Prepare the ROS 2 environment

These commands use ROS 2 Jazzy on Ubuntu. Open a terminal and source ROS 2:

```bash
source /opt/ros/jazzy/setup.bash
```

The examples use `example_interfaces`. Check that the service type is available:

```bash
ros2 interface show example_interfaces/srv/AddTwoInts
```

If it is not installed, install it with:

```bash
sudo apt update
sudo apt install ros-jazzy-example-interfaces
```

In each new terminal, source ROS 2 before running the examples:

```bash
source /opt/ros/jazzy/setup.bash
```

## 2. Understand the service type

`AddTwoInts` defines two request fields and one response field:

```text
int64 a
int64 b
---
int64 sum
```

The fields before `---` are sent by the client. The field after `---` is returned by the server. View the full definition at any time with:

```bash
ros2 interface show example_interfaces/srv/AddTwoInts
```

## 3. Create the service server

Open `Server.py` and follow the server structure:

1. Import `rclpy`, `Node`, and `AddTwoInts`.
2. Define a node class derived from `Node` and give it a valid node name.
3. In the constructor, call `create_service()` with the service type, service name, and callback.
4. In the callback, read `request.a` and `request.b`, set `response.sum`, and return the response.
5. In `main()`, initialize ROS, create the node, and call `rclpy.spin(node)` so the server remains available for requests.

The core server code is:

```python
self.server_ = self.create_service(
    AddTwoInts, 'add_two_ints', self.callback_service
)

def callback_service(self, request, response):
    response.sum = request.a + request.b
    return response
```

Run the server in **Terminal 1** from this directory:

```bash
python3 Server.py
```

Leave it running while you try a client. The service name is `/add_two_ints`.

## 4. Create and run a simple client (without a node class)

Open `Client.py`. This client creates a `Node` directly inside `main()` rather than defining its own node subclass:

1. Create a node with `Node("add_two_ints_client")`.
2. Create a client for the same service type and name as the server: `AddTwoInts` and `/add_two_ints`.
3. Use `wait_for_service()` so the request is not sent before the server is available.
4. Create an `AddTwoInts.Request`, fill in `a` and `b`, then call `call_async()`.
5. Spin until the future completes, read `response.sum`, and shut down the node.

Run it in **Terminal 2** while the server is running:

```bash
python3 Client.py
```

The example requests `3 + 4`; the client should print `Sum: 7`, and the server should log the request.

## 5. Create and run a class based client (with OOP methods)

Open `Client Oop.py`. This version defines `MyCustomNode(Node)` and keeps the client and callbacks as methods on that class:

1. Create the node class and initialize its service client in `__init__()`.
2. In `wait_service(a, b)`, wait until `/add_two_ints` is available.
3. Fill in an `AddTwoInts.Request` and send it with `call_async()`.
4. Register `self.callback` to process the response when the future completes.
5. In `main()`, initialize ROS, create `MyCustomNode`, make requests, spin the node to process the callbacks, and cleanly shut down.

Stop the simple client if it has finished, then run this version in **Terminal 2**:

```bash
python3 "Client Oop.py"
```

It sends two requests: `2 + 5` and `4 + 8`. The client should print `Sum: 7` and `Sum: 12`. Keep the server running in Terminal 1 until both responses appear.

## 6. Try the service from the ROS 2 command line

Keep `Server.py` running. In another sourced terminal, discover the server and its service:

```bash
ros2 node list
ros2 node info /add_two_ints_server
ros2 service list -t
ros2 service type /add_two_ints
ros2 service find example_interfaces/srv/AddTwoInts
ros2 service info /add_two_ints
```

Call the service from the command line. The request values must match the request fields shown by `ros2 interface show`:

```bash
ros2 service call /add_two_ints example_interfaces/srv/AddTwoInts "{a: 10, b: 20}"
```

The response should contain `sum: 30`, and the server terminal should log `10 + 20 = 30`.

## ROS 2 Jazzy service command reference

| Command | Purpose |
|---|---|
| `ros2 service list` | List active service names. |
| `ros2 service list -t` | List active services and their types. |
| `ros2 service type <service>` | Show the type of an active service. |
| `ros2 service find <type>` | Find active service names that use a type. |
| `ros2 service info <service>` | Show the service type and endpoint counts. |
| `ros2 service call <service> <type> '<request>'` | Send a request and display the response. |
| `ros2 interface show <package>/srv/<Type>` | Inspect the request and response fields of a service type. |
| `ros2 node list` | List active nodes. |
| `ros2 node info <node>` | Inspect a node's services and other graph connections. |
| `ros2 doctor --report` | Print information that can help diagnose the ROS environment. |
| `ros2 --help` | List available ROS 2 command groups. |

Replace the values in angle brackets with the actual service name, type, or node name. `ros2 service list` shows active endpoints; a type definition alone does not start a server.

## Troubleshooting

1. If the server does not start, confirm `ROS_DISTRO` is `jazzy` and `example_interfaces` is installed.
2. If a client keeps waiting, check that `Server.py` is still running and that both server and client use `/add_two_ints` with `example_interfaces/srv/AddTwoInts`.
3. If a CLI call fails, check the request field names and values against `ros2 interface show example_interfaces/srv/AddTwoInts`.
4. If separate terminals cannot discover each other, source `/opt/ros/jazzy/setup.bash` in both and check that their `ROS_DOMAIN_ID` values match.
5. Stop a running node with `Ctrl+C`.

For more detail, see the [ROS 2 Jazzy services tutorial](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Services/Understanding-ROS2-Services.html) and the [ROS 2 Jazzy CLI tools guide](https://docs.ros.org/en/jazzy/Concepts/Basic/About-Command-Line-Tools.html).
