#! /usr/bin/env python
import rospy
import serial
import time
from std_msgs.msg import Bool

port="/dev/ttyACM0"
ser=serial.Serial(port,9600)
ser.flushInput
status = 0

class picker_control:
    def __init__(self):
        rospy.init_node('object_picker_node')
        rospy.Subscriber('/object_picker', Bool, self.object_callback)
        rospy.spin()
        

    def fridge_callback(self, data):    
        if (data.data == True):
            self.raise_picker()

        else:
            self.lower_picker()



    def raise_picker(self):
        ser.write(b'f')
                
           

    def lower_picker(self):
        ser.write(b'r')
                    


if __name__=='__main__':
    try:
	    picker = picker_control()
	
    except rospy.ROSInterruptException:
        pass
