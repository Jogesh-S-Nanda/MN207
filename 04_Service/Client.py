"""
========================================================================================
    Template for creating a node
========================================================================================
    Author: Jogesh S Nanda
    Created: 04/10/2026
    Modified: 04/10/2026    (by Jogesh S Nanda)
========================================================================================
    Code created for class of MN207, ROS2 session (by Robotics Innovations Lab,
        Department of Design and Manufacturing, IISc).

    version : ROS2 Jazzy

Purpose:
    To create a node using class function
========================================================================================
"""
# import the rclpy library to communicate with DDS
import rclpy
# import the node class from rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts



def main(args=None):
    """
        entry point of the application
    :param args: if required can be passed in as command line arguments
    :return:
    """
    rclpy.init(args=args)

    # initialize the node
    node = Node("add_two_ints_client")
    client = node.create_client(AddTwoInts, "/add_two_ints")

    while not client.wait_for_service(timeout_sec=1.0):
        # waiting for server to start
        node.get_logger().warning("Service not available; waiting...")

    req = AddTwoInts.Request()
    req.a = 3
    req.b = 4

    # requesting call back from other node
    future = client.call_async(req)

    try:
        # spin the node until the response
        rclpy.spin_until_future_complete(node, future)

        if future.done():
            error = future.exception()

            if error is None:
                response = future.result()
                node.get_logger().info(f"Sum: {response.sum}")
            else:
                node.get_logger().error(f"Service call failed: {error}")
        else:
            node.get_logger().error("Service call did not complete")

    finally:
        # killing the node
        node.destroy_node()

        if rclpy.ok():
            # clean shutdown
            rclpy.shutdown()


if __name__ == '__main__':
    # entry point of the program when this Python file is called
    main()
