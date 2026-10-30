"""
========================================================================================
    Code for creating an Action client
========================================================================================
    Author: Jogesh S Nanda
    Created: 30/10/2026
    Modified: 30/10/2026    (by Jogesh S Nanda)
========================================================================================
    Code created for class of MN207, ROS2 session (by Robotics Innovations Lab,
        Department of Design and Manufacturing, IISc).

    version : ROS2 Jazzy

Purpose:
    To create a Action client node using class function
========================================================================================
"""

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from custom_interfaces.action import DriveDistance

class SampleActionClient(Node):
    """
    Send a mobile robot a drive-distance action goal.
    """

    def __init__(self) -> None:
        """
        Name the node and create the action client.
        """
        super().__init__("drive_distance_client")

        # create an action client with the server which needs to be connected
        self.goal_handler_ = None
        self.drive_client_ = ActionClient(self, DriveDistance, "drive_distance")


    def send_goal(self, distance_m, speed_mps):
        """
            send the goal to the server
        :param distance_m: distance for the robot to travel, in metres
        :param speed_mps: requested speed, in metres per second
        :return: none
        """
        # wait for server
        self.drive_client_.wait_for_server()

        # create a goal
        target = DriveDistance.Goal()
        target.distance_m = float(distance_m)
        target.speed_mps = float(speed_mps)

        # send the goal
        # .send_goal() - blocking method
        # .send_goal_async() - non-blocking method
        self.get_logger().info("Sending goal to server")
        self.drive_client_.send_goal_async(
            target, feedback_callback=self.feedback_callback
        ).add_done_callback(self.goal_callback)

    def feedback_callback(self, feedback_message):
        feedback = feedback_message.feedback
        self.get_logger().info(
            f"Travelled {feedback.distance_travelled_m:.2f} m; "
            f"{feedback.remaining_distance_m:.2f} m remaining"
        )


    def goal_callback(self, future):
        """
            callback function from server to check if goal is accepted or not.
        :param future: function return when triggered from server
        :return: none
        """
        # initialize the goal handler
        self.goal_handler_: ActionClient.ClientGoalHandle = future.result()

        if self.goal_handler_.accepted:
            # if the goal is accepted then adding future object for getting results
            self.get_logger().info("Goal accepted")
            self.goal_handler_.get_result_async().add_done_callback(self.result_callback)
        else:
            self.get_logger().warning("Goal rejected")


    def result_callback(self, future):
        """
            callback function from server to get the result.
        :param future: function return when triggered from server
        :return: result from server
        """
        results = future.result().result
        self.get_logger().info(
            f"Drive finished: success={results.success}, "
            f"distance={results.distance_travelled_m:.2f} m, message={results.message}"
        )





def main(args=None) -> None:
    """
    Initialize ROS, run the demo node, and clean up on exit.
    """
    rclpy.init(args=args)
    node = SampleActionClient()
    node.send_goal(distance_m=1.0, speed_mps=0.2)

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
