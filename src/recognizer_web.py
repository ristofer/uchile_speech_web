#!/usr/bin/env python

import roslib
import rospy
import actionlib
import speech_recognition as sr

from uchile_speech_web.msg import DoRecognitionAction, DoRecognitionResult, CalibrateThresholdAction, CalibrateThresholdResult

class SpeechRecognitionServer:
	def __init__(self):
		self.recognition_server = actionlib.SimpleActionServer('recognizer/recognizer_action', DoRecognitionAction, self.execute, False)
		self.threshold_server = actionlib.SimpleActionServer('calibrate_threshold',CalibrateThresholdAction,self.calibrate,False)
		self.recognition_server.start()
		self.threshold_server.start()
		self.recognizer = sr.Recognizer()
		self.recognizer.operation_timeout = 12.0
		self.is_recognizing = False

		self.recognition_response = DoRecognitionResult()
		self.calibrate_response = CalibrateThresholdResult()

	def execute(self, goal):
		self.is_recognizing = True
		with sr.Microphone() as source:
			print('Reconociendo')
			audio = self.recognizer.listen(source)
			print('Listoco')
		try:
			recognized_sentence=self.recognizer.recognize_google(audio)
			self.recognition_response.final_result = recognized_sentence
			self.recognition_server.set_succeeded(self.recognition_response)
			print ('Recognized: ' + recognized_sentence)
			self.is_recognizing = False
			return
		except sr.UnknownValueError:
			print("Google Speech Recognition could not understand audio")
		except sr.RequestError as e:
			print("Could not request results from Google Speech Recognition service; {0}".format(e))


	def calibrate(self,goal):
		duration = 1.0
		if goal.duration > 1.0 :
			duration = goal.duration
		if self.is_recognizing:
			self.threshold_server.set_preempted()
			print('The recognizer is recognizing')
			return

		with sr.Microphone() as source:
			print('Calibrating...')
			self.recognizer.adjust_for_ambient_noise(source,duration=duration)
		self.threshold_server.set_succeeded()
		print('OK!')
		return




if __name__ == '__main__':
	rospy.init_node('speech_recognition_web')
	server = SpeechRecognitionServer()
	rospy.spin()
