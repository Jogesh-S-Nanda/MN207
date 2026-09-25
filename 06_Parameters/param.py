"""
========================================================================================
    Code for creating a node
========================================================================================
    Author: Jogesh S Nanda
    Created: 04/05/2020
    Modified: 04/05/2020    (by Jogesh S Nanda)
========================================================================================
    Code created for class of MN207, ROS2 session (by Robotics Innovations Lab,
        Department of Design and Manufacturing, IISc).

    version : ROS2 Jazzy

Purpose:
    To create a node using class function
========================================================================================
"""

import rclpy
from rclpy.node import Node


class TemperatureSensor(Node):
    """
    Demonstrate a timer callback using an incrementing counter.
        The counter is example data only; this node does not read a physical
    temperature sensor.
    """

    def __init__(self) -> None:
        """Name the node, initialize its demo counter, and start its timer."""
        super().__init__("temp_sensor")

        self.declare_parameter("counter", 0)
        self.counter = self.get_parameter("counter").value

        # Run timer_callback once per second while the node is being spun.
        self.declare_parameter("timer_callback", 1.0)
        self.timer1 = self.get_parameter("timer_callback").value
        self.timer = self.create_timer(self.timer1, self.timer_callback)
        self.get_logger().info("Temperature demo node started.")

    def timer_callback(self) -> None:
        """Log the current example value, then increment for the next call."""
        self.get_logger().info(f"Demo temperature reading: {self.counter}")
        self.counter += 1


def main(args=None) -> None:
    """
    Initialize ROS, run the temperature demo node, and clean up on exit.
    """
    rclpy.init(args=args)
    node = TemperatureSensor()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        # Ctrl+C is the normal way to stop this continuously running example.
        pass

    finally:
        # clean exit
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
