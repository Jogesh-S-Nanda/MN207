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
    To create a node
========================================================================================
"""

import rclpy
from rclpy.node import Node


def main(args=None) -> None:
    """
    Initialize ROS, create the node, and keep it alive until stopped.
    """
    rclpy.init(args=args)

    # This basic example creates a node directly, without defining a subclass.
    node = Node("node_A")
    try:
        node.get_logger().info("Hello, ROS 2!")
        rclpy.spin(node)

    except KeyboardInterrupt:
        # Ctrl+C is the usual way to stop a spinning ROS node from a terminal.
        pass

    finally:
        # clean exit
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
