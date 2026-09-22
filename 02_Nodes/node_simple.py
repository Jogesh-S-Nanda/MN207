import rclpy
from rclpy.node import Node

def main(args=None):
    # initialize
    rclpy.init(args=args)

    # program
    # create a node called: node_A
    node = Node('node_A')
    node.get_logger().info('Hello World!')

    rclpy.spin(node)

    # terminate the node
    rclpy.shutdown()


if __name__ == '__main__':
    main()