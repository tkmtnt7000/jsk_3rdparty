#!/usr/bin/env python

import rospy
import argparse
import csv
import json
import os
import sys

from dialogflow_task_executive.msg import DialogResponse


class DialogResponseSaver:
    def __init__(self, robot_name):
        rospy.Subscriber(
            "/dialog_response", DialogResponse, self._saver_cb, queue_size=1)
        self.save_word = []
        self.file_path = "{}.csv".format(robot_name)
        rospy.loginfo("responssaver initialized")
        rospy.loginfo("output file:{}".format(self.file_path))

    def _saver_cb(self, msg):
        if msg.action == "input.welcome":
            rospy.loginfo("input.welcome is input")
        elif msg.action == "input.unknown":
            rospy.loginfo("input.unknow is input")
            rospy.loginfo("append to word list")
            self.save_word.append(msg.query)
        else:
            self.save_word.append(msg.query)
            rospy.loginfo("write word data to csv")
            rospy.loginfo("action:{}".format(msg.action))
            rospy.loginfo("query:{}".format(self.save_word))
            self._csv_save(self.save_word, msg.action, msg.header.stamp, self.file_path)
            self.save_word = []
            # self._json_save(self.save_word, msg.action, msg.header.stamp, self.file_path)
        rospy.loginfo("save_word:{}".format(self.save_word))

    def _csv_save(self, save_content, action, timestamp, file_path):
        if not os.path.isfile(file_path):
            rospy.logerr("{} does not exist. Please create.".format(file_path))
            sys.exit(1)
        else:
            with open('{}'.format(file_path), 'a', newline='') as f:
                write_object = csv.writer(f)
                for word in save_content:
                    rospy.loginfo("loop_word:{}".format(word))
                    word_list = [timestamp, word, action]
                    write_object.writerow(word_list)
                f.close()


    # def _json_save(self, save_content, action):
    #     for word in save_content:
    #         d['action'] = 

if __name__ == '__main__':
    rospy.init_node("dialog_response_saver")
    parser = argparse.ArgumentParser(description="input robot name")
    parser.add_argument('arg1', help='output file name')
    args = parser.parse_args()
    drs = DialogResponseSaver(robot_name=args.arg1)
    rospy.spin()
