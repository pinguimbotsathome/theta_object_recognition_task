#!/usr/bin/env python3
import rospy
import rospkg
import sys
import os
import cv2
import os.path
import time
from datetime import datetime
from theta_speech.srv import SpeechToText
from std_msgs.msg import String, Empty


PACK_DIR = rospkg.RosPack().get_path("theta_speech_object_recognition_task")
LOG_DIR = os.path.join(PACK_DIR,"logs/")

tts_pub  = rospy.Publisher('/textToSpeech', String, queue_size=10)
face_pub = rospy.Publisher('/hri/affective_loop', String, queue_size=10)
hotword_pub = rospy.Publisher('/hotword_activate', Empty, queue_size=1)
object_pub = rospy.Publisher('/object_detect', Empty, queue_size=1)

def log(text, log_name, print_text=False, show_time=True):
    now = datetime.now()

    with open(log_name, "a+") as log_file:
        log_text = now.strftime(f"[%H:%M:%S] {text}") if show_time else text
        log_file.write(f"{log_text}\n")

    if print_text:
        print(text)

def object_detect():
    now = datetime.now()

    log_dir = os.path.join(PACK_DIR,"logs/")
    log_name = now.strftime("log_%H_%M_%S.txt")
    log_name = os.path.join(log_dir,log_name)

    log("Starting Object Recognition", log_name)

    tts_pub.publish('Start recognition')
    face_pub.publish('littleHappy')
    time.sleep(5)

    rospy.logwarn("Waiting recognition")
    object_pub.publish()


if __name__ == "__main__":
    rospy.init_node("Object_recognition_task")

    rospy.Subscriber("hotword", Empty, object_detect)

    while not rospy.is_shutdown():
        pass

