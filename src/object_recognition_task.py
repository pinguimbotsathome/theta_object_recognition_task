#!/usr/bin/env python3

import rospy
import time
from theta_speech.srv import SpeechToText
from theta_object_detect.srv import ObjectDetect, ObjectDetectResponse
from std_msgs.msg import String, Empty

tts_pub  = rospy.Publisher('/textToSpeech', String, queue_size=10)
face_pub = rospy.Publisher('/hri/affective_loop', String, queue_size=10)
hotword_pub = rospy.Publisher('/hotword_activate', Empty, queue_size=1)
object_pub = rospy.Publisher('/object_detect', Empty, queue_size=1)

def object_detect(self):
    #log("Starting Object Recognition", log_name)
    tts_pub.publish('Start recognition')
    #face_pub.publish('littleHappy')
    time.sleep(3)

    rospy.logwarn("Waiting recognition")
    rospy.wait_for_service("services/objectDetection")
    object_detection =  rospy.ServiceProxy("services/objectDetection", ObjectDetect)
    name_object = object_detection()
    tts_pub.publish(f"i see {name_object.n_objects} objects in the shelves")
    
    #log("Number of objects detected", log_name)
    time.sleep(2)
    tts_pub.publish(f"i see {name_object.object_list}")


if __name__ == "__main__":
    rospy.init_node("Object_recognition_task")
    rospy.Subscriber("hotword", Empty, object_detect)
    while not rospy.is_shutdown():
        pass

