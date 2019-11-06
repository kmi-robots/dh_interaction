#!/usr/bin/env python

import rospy
import tf
from tf.transformations import random_quaternion
import requests
from requests.auth import HTTPBasicAuth
import datetime
import actionlib
from geometry_msgs.msg import Twist
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import PoseStamped, Quaternion
from std_srvs.srv import SetBool

teamid = "kmirobots"
teamkey = "0e920c05-e7a0-4745-9e94-eff7e1343b5d"

# waypoints = [[0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0]]
waypoints = [[-5.1, 6.86], [-9.12, 6.5], [-13.2, 6.02], [-17.2, 5.86], [0.0, 10.0]]

if __name__ == '__main__':
    rospy.init_node("simple_navigation_exploration")

    pub_vel = rospy.Publisher("/mobile_base/commands/velocity", Twist, queue_size=1)
    trigger_client = rospy.ServiceProxy("/start_exploration", SetBool)
    nav_client = actionlib.SimpleActionClient("move_base", MoveBaseAction)
    rospy.loginfo("waiting for action server")
    nav_client.wait_for_server()

    rospy.loginfo("node started")

    for w in waypoints:
        rospy.loginfo("send goal")
        goal_pose = MoveBaseGoal()
        goal_pose.target_pose.header.frame_id = "/map"
        goal_pose.target_pose.header.stamp = rospy.Time.now()
        goal_pose.target_pose.pose.position.x = w[0]
        goal_pose.target_pose.pose.position.y = w[1]
        goal_pose.target_pose.pose.orientation = Quaternion(0.0, 0.0, 0.0, 1.0)
        nav_client.send_goal(goal_pose)
        nav_client.wait_for_result()

        t0 = rospy.Time.now()

        rospy.loginfo("starting exploration")
        trigger_client(True)
        while rospy.Time.now() - t0 < rospy.Duration(10):
            cmd = Twist()
            cmd.angular.z = 0.3
            pub_vel.publish(cmd)
            rospy.sleep(0.1)
        trigger_client(False)



