#!/usr/bin/env python3
import rospy
import rospkg
import os
import os.path
import time
from datetime import datetime
from theta_speech.srv import SpeechToText
from theta_object_detect.srv import ObjectDetect, ObjectDetectResponse
from std_msgs.msg import String, Empty


PACK_DIR = rospkg.RosPack().get_path("theta_speech_object_recognition_task")
LOG_DIR = os.path.join(PACK_DIR,"logs/")

tts_pub  = rospy.Publisher('/textToSpeech', String, queue_size=10)
face_pub = rospy.Publisher('/hri/affective_loop', String, queue_size=10)
hotword_pub = rospy.Publisher('/hotword_activate', Empty, queue_size=1)
object_pub = rospy.Publisher('/object_detect', Empty, queue_size=1)

def object_detect():
    now = datetime.now()

    log_dir = os.path.join(PACK_DIR,"logs/")
    log_name = now.strftime("log_%H_%M_%S.txt")
    log_name = os.path.join(log_dir,log_name)

    #log("Starting Object Recognition", log_name)

    tts_pub.publish('Start recognition')
    face_pub.publish('littleHappy')
    time.sleep(5)

    rospy.logwarn("Waiting recognition")
    object_pub.publish()
    rospy.wait_for_service("services/objectDetection")
    object_detection =  rospy.ServiceProxy("services/objectDetection", ObjectDetect)
    name_object = object_detection()
    tts_pub.publish(f"i see {name_object.n_objects} in the shelves")
    
    #log("Number of objects detected", log_name)
    time.sleep(2)
    tts_pub.publish(f"i see {name_object.list_object}")


if __name__ == "__main__":
    rospy.init_node("Object_recognition_task")

    rospy.Subscriber("hotword", Empty, object_detect)

    while not rospy.is_shutdown():
        pass

