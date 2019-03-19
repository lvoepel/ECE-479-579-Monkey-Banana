#!/usr/bin/env python

# Speech Synthesis Script
# V1.0
# Created by Scott Matsuo for Intelligent Robotics 1 Project 2
# Last Update - 12/03/2018
#
#
# Service Requests
# /phrase - String
#
# Service Response
# /status - int32

from speech_synthesis.srv import synthesis_service
import rospy
import boto3
import csv
import playsound

with open('credentials.csv') as csv_file:
	data = list(csv.reader(csv_file))
	key_id = data[1][2]
	secret_key = data[1][3]

polly_client = boto3.Session(
	aws_access_key_id=key_id,
	aws_secret_access_key=secret_key,
	region_name='us-west-2').client('polly')

def handle_speech_synthesis(req):
	response = polly_client.synthesize_speech(VoiceId='Hans',
				OutputFormat='mp3', 
				Text = str(req.req))
	file = open('speech.mp3', 'w')
	file.write(response['AudioStream'].read())
	file.close()
	playsound.playsound('speech.mp3', True)
 	return 1
	
def speech_synthesis_server():
	rospy.init_node('speech_synthesis_server')
	s = rospy.Service('speech_synthesis', synthesis_service, handle_speech_synthesis)
	print("Ready to synthesize.")	
 	rospy.spin()

if __name__ == "__main__":
	speech_synthesis_server()
