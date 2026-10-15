**Author:** Jogesh S Nanda, Robotics Innovation Lab (RIL), IISc  
**Purpose:** MN207 lab session  
**Copyright:** © Robotics Innovation Lab (RIL), IISc


## creating a package

mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
ros2 pkg create --build-type ament_python turtle_room_env --dependencies rclpy geometry_msgs turtlesim nav_msgs std_msgs


## runngin the package

cd ~/ros2_ws
colcon build --packages-select turtle_room_env
source install/setup.bash
ros2 run turtle_room_env room_simulator

