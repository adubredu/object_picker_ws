#! /usr/bin/env python
import rospy
import time
from std_msgs.msg import Bool
import speech_recognition as sr



class object_picker_voice:

	

		####################################
  		# SPEECH RECOGNITION METHODS	####
  		####################################

  		def setup_speech(self):
		    print "in speech setup"
		    self.rec.pause_threshold = .5
		    self.rec.dynamic_energy_threshold = False
		    with self.mic as source:
		        self.rec.adjust_for_ambient_noise(source, 3)


		def speech_callback(self, recognizer, audio):
		    # Defining Commands to be accepted
		    global t2s, dialog
		    
		    sens = 1
		    commands = ["raise", "lower"]
		    dialog = "Listening..."
		    print("listening")
		    try:
		        commandIter = [command[0] for command in commands]
		        global rawCommand
		        rawCommand = recognizer.recognize_google_cloud(audio_data=audio, language='en-US', preferred_phrases=commands)
		        dialog = rawCommand
		        print("understood")
		        print(dialog)
		        self.interprete_commands(rawCommand)

		    except sr.UnknownValueError:
		        dialog = "Listening..."
		        pass
		    except sr.RequestError as e:
		        print("Recognition error; {}".format(e))


		def interprete_commands(self, command):
			if 'raise' in command:
				com = Bool()
				com.data = True
				print('raising')
				self.pickerpub.publish(com)

			elif 'lower' in command:

				com = Bool()
				print('lowering')
				com.data = False
				self.pickerpub.publish(com)




		def __init__(self):
			rospy.init_node('voice_picker_node', disable_signals=True)
			self.pickerpub = rospy.Publisher('/object_picker', Bool, queue_size=1)
			#Speech recognition variables
			self.rec = sr.Recognizer()
			self.mic = sr.Microphone()
			self.setup_speech()
			self.stopListening = self.rec.listen_in_background(self.mic, self.speech_callback, phrase_time_limit=4)
			rospy.spin()
			
			


if __name__=="__main__":
	
	try:
		go = object_picker_voice()

	except rospy.ROSInterruptException: pass


