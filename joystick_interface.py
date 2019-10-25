#! /usr/bin/env python
import rospy
import serial
import time
from sensor_msgs.msg import Joy

port="/dev/ttyACM0"
ser=serial.Serial(port,9600)
ser.flushInput
status = 0


class joystick_interface:
	def __init__(self):
		rospy.init_node('joystick_interface_node')
		self.direction = 0
		rospy.Subscriber('/joy', Joy, self.joy_callback)
		self.run_elevator()
		rospy.spin()


	def joy_callback(self,data):
		self.direction = data.axes[1]
		print(self.direction)



	def raise_picker(self):
		ser.write(b'f')
		# print('raising')
                
           

	def lower_picker(self):
		ser.write(b'r')
		# print('lowering')


	def stop_moving(self):
		ser.write(b's')
		# print('stopping')

	def run_elevator(self):
		while not rospy.is_shutdown():
			if self.direction == 1:
				self.raise_picker()
			elif self.direction == -1:
				self.lower_picker()
			elif self.direction == 0:
				self.stop_moving()
			time.sleep(0.5)

                    


if __name__=='__main__':
	try:
		joy = joystick_interface()
	
	except rospy.ROSInterruptException:
		pass
