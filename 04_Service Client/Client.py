"""
========================================================================================
    Template for creating a node
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
    node = node("node name")

    client = node.create_client(AddTwoInts, "add_two_ints")

    while not client.wait_for_service(timeout_sec=1.0):
        node.get_logger().warn("Service not available, waiting again...")

    req = AddTwoInts.Request()
    req.a = 3
    req.b = 4

    future = client.call_async(req)

    # spin the node until the response
    rclpy.spin_until_future_complete(node, future)

    resp = future.result()
    node.get_logger().info(str(resp.sum))

    # clean exit
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    # entry point of the program when this Python file is called
    main()