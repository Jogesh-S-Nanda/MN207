"""
========================================================================================
    Code for Publishing a topic
========================================================================================
    Author: Jogesh S Nanda
    Created: 04/05/2020
    Modified: 04/05/2020    (by Jogesh S Nanda)
========================================================================================
    Code created for class of MN207, ROS2 session (by Robotics Innovations Lab,
        Department of Design and Manufacturing, IISc).

    version : ROS2 Jazzy

Purpose:
    Publish a changing temperature message every 0.1 seconds.
========================================================================================
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class TemperaturePublisher(Node):
    """
    Publish a changing temperature message every 0.1 seconds.
    """

    def __init__(self) -> None:
        """Set up the node, its publisher, and its periodic timer."""
        super().__init__("temp_sensor")

        # The message type (String), topic name (sensor), and queue depth
        # (10) must match what subscribers expect.
        self.publisher_ = self.create_publisher(String, "sensor", 10)

        # This counter supplies demonstration data; it is not a sensor value.
        self.counter = 0

        # ROS calls timer_callback every 0.1 seconds (10 times per second).
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.get_logger().info("Temperature publisher started on 'sensor'.")

    def timer_callback(self) -> None:
        """Build and publish the next simulated temperature reading."""
        msg = String()
        msg.data = f"Temperature: {self.counter} °C"
        self.publisher_.publish(msg)
        self.get_logger().info(f"Published: {msg.data}")

        # Update the instance counter so the next message has a new value.
        self.counter += 1


def main(args=None) -> None:
    """
    Initialize ROS, run the publisher, then release resources cleanly.
    """
    rclpy.init(args=args)
    node = TemperaturePublisher()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        # Ctrl+C is the normal way to stop this continuously running demo.
        pass

    finally:
        # clean exit
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    # entry point for external source pointers
    main()
