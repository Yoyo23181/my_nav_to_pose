import math
from enum import IntEnum

from geometry_msgs.msg import PoseStamped, PoseWithCovarianceStamped

from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult

import rclpy
from rclpy.qos import qos_profile_sensor_data, qos_profile_system_default
from rclpy.duration import Duration

class HuskyDirections(IntEnum):
    NORTH = 0
    NORTH_WEST = 45
    WEST = 90
    SOUTH_WEST = 135
    SOUTH = 180
    SOUTH_EAST = 225
    EAST = 270
    NORTH_EAST = 315

class HuskyNavigator(BasicNavigator):
    creating_path = False
    def __init__(self):
        super().__init__()
        self.create_subscription(PoseWithCovarianceStamped,
                                 'initialpose',
                                 self._poseEstimateCallback,
                                 qos_profile_sensor_data)
    def getPoseStamped(self, position, rotation):

        pose = PoseStamped()

        pose.header.frame_id = 'map'
        pose.header.stamp = self.get_clock().now().to_msg()

        pose.pose.position.x = position[0]
        pose.pose.position.y = position[1]

        pose.pose.orientation.z = math.sin(math.radians(rotation)/2)
        pose.pose.orientation.w = math.cos(math.radians(rotation)/2)

        return pose


    def stampPose(self, pose):
        """
        Stamp a Pose message and return a PoseStamped message.

        :param pose: Pose message
        :return: PoseStamped message
        """
        poseStamped = PoseStamped()

        poseStamped.header.frame_id = 'map'
        poseStamped.header.stamp = self.get_clock().now().to_msg()

        poseStamped.pose = pose

        return poseStamped



    def _poseEstimateCallback(self, msg: PoseWithCovarianceStamped):
        if self.creating_path:
            self.new_pose = msg.pose.pose



    def startToPose(self, pose: PoseStamped):

        i = 0
        self.goToPose(pose)

        while not self.isTaskComplete():
            feedback = self.getFeedback()
            i = i + 1
            if feedback and i%5 == 0:
                print('Estimated time of arrival: ' + '{0:.0f}'.format(
                    Duration.from_msg(feedback.estimated_time_remaining).nanoseconds / 1e9)
                      + '{0: <20}'.format('seconds.'), end='r')

                if Duration.from_msg(feedback.navigation_time) > Duration(seconds=600.0):
                    self.cancelTask()

        result = self.getResult()
        if result == TaskResult.SUCCEEDED:
            self.info('Goal succeeded!')
        elif result == TaskResult.CANCELED:
            self.info('Goal was canceled!')
        elif result == TaskResult.FAILED:
            self.info('Goal failed!')
        else:
            self.info('Goal has an invalid return status!')



def main():
    rclpy.init()

    navigator = HuskyNavigator()

    initial_pose = navigator.getPoseStamped([0.0, 0.0], HuskyDirections.NORTH)
    navigator.setInitialPose(initial_pose)

    navigator.waitUntilNav2Active()

    goal_pose = navigator.getPoseStamped([-13.0, 9.0], HuskyDirections.EAST)

    navigator.startToPose(goal_pose)

    rclpy.shutdown()


if __name__ == '__main__':
    main()




