// SweepByNumPad by Umesh Ghodke, K6VUG
// This example code is in the public domain.
// Author assumes no responsibility whatsoever.

#include <Servo.h> 

#define PWM1_MIN  700
#define PWM1_MID 1500
#define PWM1_MAX 2300

#define PWM_STEP  1
 
Servo servo1; // create servo objects to control servos
int pwm1 = 1500;      // global stores value of PWM in microseconds
// global stores value of PWM in microseconds
char inByte;          // Byte input from command prompt

void setup() 
{ 
  // initialize servo 1
  servo1.attach(5, PWM1_MIN, PWM1_MAX); // attaches the servo on pin 9 to the servo object 
  servo1.writeMicroseconds(pwm1);       // set servo to mid-point

  // initialize serial port
  Serial.begin(4800);
  Serial.println("SweepByNumPad -- Ready");
  Serial.flush();
  delay(5000);
}
 
void loop() 
{ 
  servo1.writeMicroseconds(1500);
  delay(3000);
  servo1.writeMicroseconds(2000);
  delay(3000);
}

// helper function: set servo1 pwm
void moveServo1() {
  servo1.writeMicroseconds(pwm1);
  Serial.print("Servo1 - ");
  Serial.println(pwm1);
}
