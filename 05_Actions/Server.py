"""
========================================================================================
    Code for creating an Action Server node
========================================================================================
    Author: Jogesh S Nanda
    Created: 30/10/2026
    Modified: 30/10/2026    (by Codex)
========================================================================================
    Code created for class of MN207, ROS2 session (by Robotics Innovations Lab,
        Department of Design and Manufacturing, IISc).

    version : ROS2 Jazzy

Purpose:
    To simulate a mobile robot driving a requested distance and report feedback
========================================================================================
"""
import time
import rclpy
# import from rclpy (optional)
from rclpy.action import ActionServer, GoalResponse
from rclpy.node import Node
# import the custom interfaces
from custom_interfaces.action import DriveDistance


class SampleActionServer(Node):
    """
    Simulate a mobile robot's drive-distance action server.
    """
    def __init__(self) -> None:
        """
        Initialize the action server node.
        """
        super().__init__("drive_distance_server")

        # create an action server
        self.action_server_ = ActionServer(
            self,
            DriveDistance,
            "drive_distance",
            execute_callback=self.execute_callback,
            goal_callback=self.goal_callback,
        )
        # diagnostics print in terminal
        self.get_logger().info("Action server '/drive_distance' is ready")


    def goal_callback(self, goal_request: DriveDistance.Goal) -> GoalResponse:
        """
            Accept only goals with a positive distance and speed.
        :param goal_request: custom datatype
        :return: response
        """
        if goal_request.distance_m <= 0.0 or goal_request.speed_mps <= 0.0:
            # rejection condition
            self.get_logger().warning(
                "Rejecting goal: distance_m and speed_mps must both be positive"
            )
            return GoalResponse.REJECT

        # else accepted
        self.get_logger().info(
            f"Accepting goal: drive {goal_request.distance_m:.2f} m "
            f"at {goal_request.speed_mps:.2f} m/s"
        )
        return GoalResponse.ACCEPT


    def execute_callback(self, goal_handle) -> DriveDistance.Result:
        """
            Simulate driving and publish progress until the goal is complete.
        :param goal_handle: return results
        :return:
        """
        # fetching the data from the callback function
        goal = goal_handle.request
        distance_goal = float(goal.distance_m)
        speed = float(goal.speed_mps)
        update_period = 0.2
        distance_travelled = 0.0

        self.get_logger().info("Executing drive-distance goal")

        while distance_travelled < distance_goal:
            # Pause to simulate the time taken by a mobile robot to move.
            time.sleep(update_period)

            distance_travelled = min(
                distance_travelled + speed * update_period,
                distance_goal,
            )

            feedback = DriveDistance.Feedback()
            feedback.distance_travelled_m = distance_travelled
            feedback.remaining_distance_m = distance_goal - distance_travelled
            goal_handle.publish_feedback(feedback)

            # printing in terminal for diagnostics
            self.get_logger().info(
                f"Progress: {distance_travelled:.2f} m travelled, "
                f"{feedback.remaining_distance_m:.2f} m remaining"
            )

        # execution success
        goal_handle.succeed()
        result = DriveDistance.Result()
        result.success = True
        result.distance_travelled_m = distance_travelled
        result.message = "Target distance reached"
        self.get_logger().info(result.message)
        return result



def main(args=None) -> None:
    """
        entry point of the code
    :param args: None
    :return:
    """
    rclpy.init(args=args)
    node = SampleActionServer()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:
        # kill the node
        node.destroy_node()

        if rclpy.ok():
            # clean exit
            rclpy.shutdown()


if __name__ == "__main__":
    main()
