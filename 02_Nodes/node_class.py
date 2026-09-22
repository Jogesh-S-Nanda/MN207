import rclpy
from rclpy.node import Node

class temp_sensor(Node):
    def __init__(self):
        # class constructor
        super().__init__('temp_sensor')
        self.get_logger().info('Temp sensor started!')

        # variable declaration
        self.counter = 0

        # create a timer function from ros2 functions
        self.create_timer(1.0, self.timer_callback)

    def timer_callback(self):
        self.get_logger().info('Temp sensor received!' + str(self.counter))
        self.counter = self.counter + 1



def main(args=None):
    rclpy.init(args=args)
    node = temp_sensor()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()