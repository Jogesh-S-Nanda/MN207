# ROS 2 Jazzy Data Types for Mobile Robotics

This reference covers **all built-in ROS 2 Jazzy field types** and the standard
messages, services, and actions most relevant to mobile robots.

> ROS 2 has thousands of application-specific interfaces. Here, “all data
> types” means every built-in field type plus commonly used standard robotics
> interfaces—not every type supplied by every hardware driver.

## 1. ROS 2 Interface Kinds

| Interface | File | Communication | Example |
|---|---|---|---|
| Message | `.msg` | Topic data | Laser scan, velocity, odometry |
| Service | `.srv` | Short request/response | Load a map |
| Action | `.action` | Long task with feedback/cancellation | Navigate to a pose |

A complete type name looks like `geometry_msgs/msg/Twist`.

## 2. All Built-in Field Types

| ROS 2 type | Meaning | Typical use |
|---|---|---|
| `bool` | Boolean | Motor enabled, bumper active |
| `byte` | Unsigned raw byte | Binary protocol data |
| `char` | 8-bit character | Character or code data |
| `float32` | 32-bit floating point | Laser ranges, joystick axes |
| `float64` | 64-bit floating point | Position, velocity, covariance |
| `int8` | Signed 8-bit integer | Small signed state |
| `uint8` | Unsigned 8-bit integer | Status code, image byte |
| `int16` | Signed 16-bit integer | Encoder or sensor value |
| `uint16` | Unsigned 16-bit integer | Device value |
| `int32` | Signed 32-bit integer | Counts, coordinates |
| `uint32` | Unsigned 32-bit integer | Width, height, counter |
| `int64` | Signed 64-bit integer | Large count |
| `uint64` | Unsigned 64-bit integer | Large counter |
| `string` | UTF-8 string | Frame, joint, or robot name |
| `wstring` | UTF-16 wide string | Wide text; rarely used in robots |

### Arrays, sequences, and bounded values

```text
int32[3] fixed_values          # Exactly 3 values
float64[] samples              # Unbounded sequence
uint8[<=255] packet            # At most 255 values
string frame_id                # Unbounded string
string<=32 device_name         # At most 32 characters
string<=16[<=10] labels        # Up to 10 bounded strings
```

### Constants and defaults

```text
uint8 IDLE=0                   # Constant: uses =
uint8 MOVING=1
bool enabled true              # Default: no =
string frame_id "base_link"
int32[] samples [-2, -1, 0, 1, 2]
```

## 3. Fundamental Types

### `builtin_interfaces`

| Type | Fields | Use |
|---|---|---|
| `builtin_interfaces/msg/Time` | `int32 sec`, `uint32 nanosec` | Point in ROS time |
| `builtin_interfaces/msg/Duration` | `int32 sec`, `uint32 nanosec` | Time interval |

### `std_msgs`

| Types | Use |
|---|---|
| `Header` | Timestamp and frame ID embedded in sensor/geometry messages |
| `Bool`, `Byte`, `Char`, `String`, `Empty` | Wrapped values or event signals |
| `Float32`, `Float64` | Wrapped floating-point values |
| `Int8/16/32/64`, `UInt8/16/32/64` | Wrapped integers |
| `ByteMultiArray`, `Float32MultiArray`, `Float64MultiArray` | Numeric arrays with layout metadata |
| `Int8/16/32/64MultiArray`, `UInt8/16/32/64MultiArray` | Integer arrays with layout metadata |
| `MultiArrayDimension`, `MultiArrayLayout` | Shape, stride, and offset metadata |
| `ColorRGBA` | RGBA color used in visualization |

Prefer a meaningful custom message over a generic scalar or multi-array when
the fields have clear physical meaning.

## 4. Geometry and Motion (`geometry_msgs`)

| Type | Meaning / use |
|---|---|
| `Point`, `Point32` | Cartesian position `(x, y, z)` |
| `Vector3` | Direction or magnitude vector |
| `Quaternion` | 3D orientation `(x, y, z, w)` |
| `Pose` | Position plus orientation |
| `Pose2D` | Planar `x`, `y`, `theta`; not preferred for TF |
| `Transform` | Translation plus rotation between frames |
| `Twist` | Linear and angular velocity |
| `Accel` | Linear and angular acceleration |
| `Wrench` | Force and torque |
| `Inertia` | Mass, center of mass, rotational inertia |
| `Polygon`, `PolygonInstance` | Robot footprint or region |
| `PoseArray` | Multiple poses in one frame |
| `PoseWithCovariance` | Pose with a `6 x 6` uncertainty matrix |
| `TwistWithCovariance` | Velocity with a `6 x 6` uncertainty matrix |
| `AccelWithCovariance` | Acceleration with uncertainty |
| `PointStamped`, `Vector3Stamped`, `QuaternionStamped` | Stamped values |
| `PoseStamped`, `TransformStamped`, `TwistStamped` | Stamped pose, transform, or velocity |
| `PoseWithCovarianceStamped` | Common localization output |
| `TwistWithCovarianceStamped`, `AccelWithCovarianceStamped` | Stamped uncertain motion |
| `WrenchStamped`, `InertiaStamped`, `PolygonStamped` | Stamped force, inertia, or polygon |
| `VelocityStamped` | Velocity with reference-frame metadata |

Typical differential-drive command on `/cmd_vel`:

```text
linear.x   = forward speed in m/s
linear.y   = sideways speed in m/s (normally 0)
angular.z  = yaw rate in rad/s
```

Ground robots normally use `x` forward, `y` left, and `z` up.

## 5. Transform Tree (`tf2_msgs`)

| Type | Use |
|---|---|
| `tf2_msgs/msg/TFMessage` | Array of `TransformStamped` on `/tf` or `/tf_static` |
| `tf2_msgs/msg/TF2Error` | Transform lookup error code and text |

```text
map -> odom -> base_link -> sensor frames
```

- `map -> odom`: corrected by localization or SLAM.
- `odom -> base_link`: continuous local odometry.
- `base_link -> sensor`: normally a static robot-model transform.

## 6. Sensors (`sensor_msgs`)

### Motion, position, and state

| Type | Use |
|---|---|
| `Imu` | Orientation, angular velocity, acceleration, covariances |
| `MagneticField` | 3-axis magnetometer reading |
| `NavSatFix`, `NavSatStatus` | GNSS position, status, and covariance |
| `JointState` | Joint names, positions, velocities, efforts |
| `MultiDOFJointState` | Multi-degree-of-freedom joint state |
| `BatteryState` | Voltage, current, charge, percentage, health |

### Range sensors and point clouds

| Type | Use |
|---|---|
| `LaserScan` | Single-echo planar lidar; commonly `/scan` |
| `MultiEchoLaserScan`, `LaserEcho` | Planar lidar with multiple returns |
| `Range` | Ultrasonic, infrared, or other single range |
| `PointCloud2`, `PointField` | Modern packed 3D point cloud |
| `PointCloud`, `ChannelFloat32` | Legacy; prefer `PointCloud2` |

### Cameras

| Type | Use |
|---|---|
| `Image` | Uncompressed image |
| `CompressedImage` | JPEG, PNG, or other compressed image |
| `CameraInfo` | Camera calibration and distortion data |
| `RegionOfInterest` | Rectangular image area |

### Environment, input, and timing

| Type | Use |
|---|---|
| `Temperature` | Temperature and variance |
| `FluidPressure` | Barometric/fluid pressure |
| `RelativeHumidity` | Humidity and variance |
| `Illuminance` | Light level in lux |
| `Joy` | Joystick axes and buttons |
| `JoyFeedback`, `JoyFeedbackArray` | Rumble, LED, or buzzer feedback |
| `TimeReference` | Measurement from an external clock |

Related service: `sensor_msgs/srv/SetCameraInfo` stores camera calibration.

## 7. Navigation, Odometry, and Maps (`nav_msgs`)

| Type | Important content | Use |
|---|---|---|
| `Odometry` | Pose and twist with covariance | Motion estimate; normally `/odom` |
| `OccupancyGrid` | Metadata plus signed cells | 2D map; normally `/map` |
| `MapMetaData` | Resolution, size, origin, load time | Grid description |
| `GridCells` | Cell size and occupied points | Grid representation |
| `Path` | Sequence of `PoseStamped` | Planned or recorded path |

Standard services:

| Service | Use |
|---|---|
| `GetMap` | Request an occupancy grid |
| `SetMap` | Set map and initial pose |
| `GetPlan` | Request a path between poses |
| `LoadMap` | Load a map |
| `SaveMap` | Save an occupancy grid |

`OccupancyGrid.data` normally uses `-1` for unknown, `0` for free, `100` for
occupied, and intermediate values for producer-defined probability or cost.

## 8. Localization, Mapping, and Geography

| Type | Typical use |
|---|---|
| `geometry_msgs/msg/PoseWithCovarianceStamped` | Initial/localized pose |
| `nav_msgs/msg/Odometry` | Wheel, visual, or fused odometry |
| `nav_msgs/msg/OccupancyGrid` | SLAM or map-server output |
| `map_msgs/msg/OccupancyGridUpdate` | Incremental 2D map update |
| `map_msgs/msg/PointCloud2Update` | Incremental point-map update |
| `geographic_msgs/msg/GeoPoint` | Latitude, longitude, altitude |
| `geographic_msgs/msg/GeoPoseStamped` | Globally referenced pose |
| `geographic_msgs/msg/GeoPath` | Geographic waypoint path |

Pose and twist covariance arrays have 36 row-major entries ordered as:

```text
x, y, z, rotation about x, rotation about y, rotation about z
```

## 9. Trajectory and Control Types

| Type | Use |
|---|---|
| `trajectory_msgs/msg/JointTrajectory` | Time-parameterized joint motion |
| `JointTrajectoryPoint` | Position, velocity, acceleration, effort, time |
| `MultiDOFJointTrajectory` | Multi-DOF trajectory |
| `MultiDOFJointTrajectoryPoint` | Transforms, velocities, accelerations, time |
| `control_msgs/action/FollowJointTrajectory` | Execute a joint trajectory |
| `control_msgs/msg/DynamicJointState` | Named state interfaces for joints |

A differential-drive base generally reports wheels using `JointState` and
accepts a `Twist`-based velocity command.

## 10. Nav2 Interfaces

| Action | Use |
|---|---|
| `nav2_msgs/action/NavigateToPose` | Navigate to one goal pose |
| `NavigateThroughPoses` | Navigate through ordered poses |
| `FollowWaypoints`, `FollowGPSWaypoints` | Visit local or geographic waypoints |
| `ComputePathToPose`, `ComputePathThroughPoses` | Compute paths |
| `FollowPath` | Follow a supplied path |
| `SmoothPath` | Smooth a path |
| `Spin`, `BackUp`, `DriveOnHeading`, `Wait` | Recovery/behavior operations |
| `AssistedTeleop` | Teleoperate with collision assistance |
| `DockRobot`, `UndockRobot` | Docking operations |

| Other Nav2 type | Use |
|---|---|
| `nav2_msgs/msg/Costmap`, `CostmapMetaData` | Navigation costmap |
| `BehaviorTreeLog` | Behavior-tree status changes |
| `ParticleCloud` | Localization particles |
| `SpeedLimit` | Percentage or absolute speed limit |
| `nav2_msgs/srv/ClearEntireCostmap` | Clear a complete costmap |
| `ClearCostmapAroundRobot` | Clear nearby cells |
| `ManageLifecycleNodes` | Control the Nav2 lifecycle |

## 11. Diagnostics, Visualization, and Simulation

| Type | Use |
|---|---|
| `diagnostic_msgs/msg/DiagnosticArray` | Timestamped system/device health |
| `DiagnosticStatus` | OK, WARN, ERROR, or STALE status |
| `KeyValue` | Named diagnostic property |
| `visualization_msgs/msg/Marker` | Point, line, mesh, text, or shape in RViz |
| `MarkerArray` | Multiple RViz markers |
| `InteractiveMarker` and related types | User-manipulable RViz controls |
| `shape_msgs/msg/SolidPrimitive` | Box, sphere, cylinder, cone, or prism |
| `shape_msgs/msg/Mesh` | Triangle mesh geometry |
| `rosgraph_msgs/msg/Clock` | Simulation time on `/clock` |

## 12. Common Mobile-Robot Topics

| Topic | Recommended type | Purpose |
|---|---|---|
| `/cmd_vel` | `geometry_msgs/msg/Twist` or `TwistStamped` | Velocity command |
| `/odom` | `nav_msgs/msg/Odometry` | Local odometry |
| `/scan` | `sensor_msgs/msg/LaserScan` | 2D lidar |
| `/imu/data` | `sensor_msgs/msg/Imu` | IMU data |
| `/joint_states` | `sensor_msgs/msg/JointState` | Wheel/joint state |
| `/map` | `nav_msgs/msg/OccupancyGrid` | Map |
| `/plan` | `nav_msgs/msg/Path` | Planned path |
| `/tf`, `/tf_static` | `tf2_msgs/msg/TFMessage` | Transforms |
| `/battery_state` | `sensor_msgs/msg/BatteryState` | Power state |
| `/diagnostics` | `diagnostic_msgs/msg/DiagnosticArray` | Health |
| `/clock` | `rosgraph_msgs/msg/Clock` | Simulation clock |

Topic names are conventions and can be remapped. The declared type determines
the actual data structure.

## 13. Example Custom Message

`RobotStatus.msg`

```text
std_msgs/Header header

uint8 IDLE=0
uint8 MOVING=1
uint8 BLOCKED=2
uint8 ERROR=3

string<=32 robot_name "robot_1"
uint8 state
bool motors_enabled
float32 battery_percentage
geometry_msgs/PoseWithCovariance pose
geometry_msgs/Twist velocity
sensor_msgs/Range[] proximity_sensors
string[] warnings
```

## 14. Inspect Installed Types

```bash
ros2 interface show geometry_msgs/msg/Twist
ros2 interface show sensor_msgs/msg/LaserScan
ros2 interface show nav_msgs/msg/Odometry
ros2 interface list
ros2 topic type /scan
ros2 topic echo --once /scan
```

## 15. Selection Guidelines

- Include a `Header` whenever timestamp and coordinate frame matter.
- Use SI units: metres, seconds, radians, m/s, and rad/s.
- Use quaternions for 3D orientation.
- Include covariance when uncertainty matters.
- Use `PointCloud2`, not deprecated `PointCloud`.
- Use topics for streams, services for short operations, and actions for
  long-running cancellable tasks.
- Reuse a standard interface when its semantics match; create a custom type
  only when the data has genuinely different meaning.

## References

- [ROS 2 Jazzy interface concepts](https://docs.ros.org/en/jazzy/Concepts/Basic/About-Interfaces.html)
- [Topics, services, and actions](https://docs.ros.org/en/jazzy/How-To-Guides/Topics-Services-Actions.html)
- [Jazzy common interfaces](https://docs.ros.org/en/jazzy/p/common_interfaces/)
- [Jazzy geometry messages](https://docs.ros.org/en/ros2_packages/jazzy/api/geometry_msgs/__message_definitions.html)
- [Jazzy Nav2 actions](https://docs.ros.org/en/jazzy/p/nav2_msgs/__action_definitions.html)
- [Jazzy TF2 messages](https://docs.ros.org/en/jazzy/p/tf2_msgs/__message_definitions.html)
