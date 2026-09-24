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


class MyCustomNode(Node):   # MODIFY NODE
    """
    Defining a custom node using class function
        naming is insignificant, but should be unique to each Python file.
        import the class property from Node class
    """
    def __init__(self):
        """
            definition of node name: should be unique.
        """
        super().__init__('node name')   # MODIFY NAME



def main(args=None):
    """
        entry point of the application
    :param args: if required can be passed in as command line arguments
    :return:
    """
    rclpy.init(args=args)

    # initialize the node
    node = MyCustomNode()
    # run the node till exit
    rclpy.spin(node)

    # clean exit
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    # entry point of the program when this Python file is called
    main()