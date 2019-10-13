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
		rospy.Subscriber('/joy', Joy, self.joy_callback)
		rospy.spin()


    def joy_callback(self,data):
    	if (data.axes[5] > 0):
    		self.raise_picker()

        elif (data.axes[5] < 0):
            self.lower_picker()



    def raise_picker(self):
        ser.write(b'f')
                
           

    def lower_picker(self):
        ser.write(b'r')
                    


if __name__=='__main__':
    try:
	    joy = joystick_interface()
	
    except rospy.ROSInterruptException:
        pass
