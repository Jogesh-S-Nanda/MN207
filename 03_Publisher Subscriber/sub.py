"""
========================================================================================
    Code for Subscribing a topic
========================================================================================
    Author: Jogesh S Nanda
    Created: 04/05/2020
    Modified: 04/05/2020    (by Jogesh S Nanda)
========================================================================================
    Code created for class of MN207, ROS2 session (by Robotics Innovations Lab,
        Department of Design and Manufacturing, IISc).

    version : ROS2 Jazzy

Purpose:
    Subscribe to temperature message every when available.
========================================================================================
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class TemperatureSubscriber(Node):
    """
    Receive temperature messages published on the ``sensor`` topic.
    """

    def __init__(self) -> None:
        """Create a ROS 2 subscription that listens for String messages."""
        super().__init__("temp_subscriber")

        # These must match the publisher's message type and topic name.
        # The queue depth allows ROS 2 to buffer up to 10 messages if needed.
        self.subscription = self.create_subscription(
            String,
            "sensor",
            self.listener_callback,
            10,
        )
        self.get_logger().info("Temperature subscriber listening on 'sensor'.")

    def listener_callback(self, msg: String) -> None:
        """Log each temperature message received from the publisher."""
        self.get_logger().info(f"Received: {msg.data}")


def main(args=None) -> None:
    """
    Initialize ROS, run the subscriber, and clean up when stopped.
    """
    rclpy.init(args=args)
    node = TemperatureSubscriber()

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
    # entry point when called from external pointer.
    main()
