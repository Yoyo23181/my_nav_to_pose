import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from nav2_msgs.action import NavigateToPose
from rclpy.action import ActionClient
from rclpy.qos import QoSProfile

class ControlHusky(Node):

    def __init__(self):
        super().__init__('control_husky')
        self._action_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')
        self.goal_pose = PoseStamped()

    def send_goal(self):
        self.goal_pose.header.frame_id = "map"
        self.goal_pose.header.stamp = self.get_clock().now().to_msg()

        # Define your goal position and orientation
        self.goal_pose.pose.position.x = 1.0
        self.goal_pose.pose.position.y = 2.0
        self.goal_pose.pose.orientation.z = 0.0
        self.goal_pose.pose.orientation.w = 1.0

        # Create the goal message for NavigateToPose
        goal_msg = NavigateToPose.Goal()
        goal_msg.pose = self.goal_pose

        self.get_logger().info('Waiting for action server...')
        self._action_client.wait_for_server()

        self.get_logger().info('Sending goal...')
        self._send_goal_future = self._action_client.send_goal_async(
            goal_msg, feedback_callback=self.feedback_callback)
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected :(')
            return

        self.get_logger().info('Goal accepted :)')
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result()
        if result.status == 4:  # 4 means SUCCEEDED
            self.get_logger().info('Goal reached successfully!')
        else:
            self.get_logger().info('Goal failed with status: {0}'.format(result.status))

        rclpy.shutdown()

    def feedback_callback(self, feedback_msg):
        self.get_logger().info('Received feedback: {0}'.format(feedback_msg.feedback))

def main(args=None):
    rclpy.init(args=args)
    node = ControlHusky()
    node.send_goal()
    rclpy.spin(node)

if __name__ == '__main__':
    main()
