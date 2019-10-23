#!/usr/bin/env python  

import rospy
import tf
import requests
from requests.auth import HTTPBasicAuth
import datetime

teamid = "kmirobots"
teamkey = "0e920c05-e7a0-4745-9e94-eff7e1343b5d"
pose_url = ""

url = "https://api.mksmart.org/sciroc-competition/kmirobots/sciroc-robot-location/"


def query_pose(event):
    global pose_url
    try:
        (trans, rot) = listener.lookupTransform('/odom', '/base_link', rospy.Time(0))
        
        t0 = datetime.datetime.fromtimestamp(rospy.Time.now().secs)
        timestamp = t0.strftime("%Y-%m-%dT%H:%M:%SZ")
        
        payload = "  {\n    \"@id\": \""+pose_id+"\",\n    \"@type\": \"RobotLocation\",\n    \"episode\": \"EPISODE12\",\n    \"team\": \"kmirobots\",\n    \"timestamp\": \""+timestamp+"\",\n    \"x\": "+str(trans[0])+",\n    \"y\": "+str(trans[1])+",\n    \"z\": "+str(trans[2])+"\n}"
        rospy.loginfo(payload)
        
        complete_url = url + pose_id
        
        response = requests.request("POST", complete_url, data=payload, auth=HTTPBasicAuth(teamkey, ''))
        rospy.loginfo(response.text)
    except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
        pass


if __name__ == '__main__':
    
    rospy.init_node('send_pose')
    
    t = rospy.Time.now()
    pose_id = "pose_"+str(t.secs)+"_"+str(t.nsecs)

    listener = tf.TransformListener()
    
    rospy.Timer(rospy.Duration(1), query_pose)
    
    rate = rospy.Rate(10.0)
    while not rospy.is_shutdown():
        rate.sleep()
