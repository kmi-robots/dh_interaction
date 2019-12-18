#!/usr/bin/env python

import rospy
import actionlib
from geometry_msgs.msg import Twist, Quaternion
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from dh_interaction.msg import explorationAction, explorationGoal
from std_srvs.srv import SetBool

# activities 0 - 2
waypoints = [[35.2, 17.4], [35.2, 14.4], [35.2, 12.5], [30.9, 16.6], [30.5, 14.3], [31.3, 12.4], [26.9, 16.6], [25.3, 14.1], [27.2, 12], [26.3, 19.9]]

# activities 3 - 5
#waypoints = [[22.6, 16.1], [22.3, 13.7], [23, 11.8], [18.5, 15.9], [19.3, 13.5], [18.7, 11.6], [14.4, 15.5], [14.2, 12.9], [14.7, 11], [26.3, 19.9]]

if __name__ == '__main__':
    rospy.init_node("simple_navigation_exploration")

    pub_vel = rospy.Publisher("/mobile_base/commands/velocity", Twist, queue_size=1)
    # trigger_client = rospy.ServiceProxy("start_exploration", SetBool)
    trigger_client = actionlib.SimpleActionClient("exploration", explorationAction)
    nav_client = actionlib.SimpleActionClient("move_base", MoveBaseAction)
    rospy.loginfo("waiting for action server")
    nav_client.wait_for_server()
    trigger_client.wait_for_server()

    rospy.loginfo("node started")

    for w in waypoints:
        rospy.loginfo("send goal")
        goal_pose = MoveBaseGoal()
        goal_pose.target_pose.header.frame_id = "map"
        goal_pose.target_pose.header.stamp = rospy.Time.now()
        goal_pose.target_pose.pose.position.x = w[0]
        goal_pose.target_pose.pose.position.y = w[1]
        goal_pose.target_pose.pose.orientation = Quaternion(0.0, 0.0, 0.0, 1.0)
        # nav_client.send_goal(goal_pose)
        # nav_client.wait_for_result()

        rospy.loginfo("starting exploration")
        exp = explorationGoal()
        exp.duration = 10
        exp.mode = 0
        cmd = Twist()
        cmd.angular.z = 0.0
        trigger_client.send_goal(exp)

        while not trigger_client.wait_for_result(rospy.Duration(0, 100000000)):
            pub_vel.publish(cmd)

        rospy.loginfo("exploration completed")