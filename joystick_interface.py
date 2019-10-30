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
        self.open = None
        self.close = None
        rospy.Subscriber('/joy', Joy, self.joy_callback)
        self.run_elevator()
        rospy.spin()


    def joy_callback(self,data):
        self.direction = data.axes[1]
        self.open = data.buttons[0]
        self.close = data.buttons[4]

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

    def control_pick_up(self):
        if self.open == 1:
                ser.write(b'o')
        elif self.close == 1:
                ser.write(b'c')

    def run_elevator(self):
        while not rospy.is_shutdown():
            if self.direction == 1:
                self.raise_picker()
            elif self.direction == -1:
                self.lower_picker()
            elif self.direction == 0:
                self.stop_moving()
            self.control_pick_up()
                        
            time.sleep(0.5)

                    


if __name__=='__main__':
    try:
        joy = joystick_interface()
    
    except rospy.ROSInterruptException:
        pass
