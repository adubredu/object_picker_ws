//HS785HB Servo step input controller

/**
 * Servo response has noticable latency when stopping or changing direction probably because the delay between steps in position
 * is too small to the servo can't keep up with the loop. When the stop command is given, the unfinished stepping loops still need
 * to finish. Chenlu recommends delat of at least 10-20 ms. The high torque on the servo also probaly causes slow deceleration,
 * because servo has a greater range of torque to decrease when approaching the desired position. Smaller torque would probably
 * decrease the deceleration time
  */

#include <Servo.h>
Servo myservo;  // create servo object to control a servo 
Servo pickservo;
char user_input = 's'; //String captured from serial port
char state = 's';
int n; //value to write to servo
int direc=1; //multiplier for direction of change in position (1 for forward, -1 for reverse, 0 for no motion)
int INITPOS = 1000;
int MINPOS = 1000;
int MAXPOS = 1900;
int STEPSIZE = 40; //
String print_message;



void open_picker()
{
   pickservo.writeMicroseconds(500);
}


void close_picker()
{
  pickservo.writeMicroseconds(2500);
}


void setup() {
  Serial.begin(9600);
  n = INITPOS;
  myservo.writeMicroseconds(n); //set initial servo position if desired
  myservo.attach(9, MINPOS, MAXPOS);  //the pin for the servo control, and range if desired
  pickservo.attach(5);
  pickservo.writeMicroseconds(2500);

  
  setState('s');
//  Serial.println();
//  Serial.println("Input 'f' or 'r' to step motor by one step (1 degree)");
//  Serial.println("Input 's' to stop motor movement");
}

void loop() {
  if (Serial.available()) {
    user_input = Serial.read();
  
    if (user_input != state)
    {
      setState(user_input);
    }
    if (n >= MINPOS and n <= MAXPOS) {
      n = n + (direc * STEPSIZE);
      myservo.writeMicroseconds(n);
      

      if (n < MINPOS or n > MAXPOS) {
        setState('s');
        if (n < MINPOS) {
          n = MINPOS;
        }
        else {
          n = MAXPOS;
        }
      }


      delay(100);
    }
  }
}

void setState(char inputState)
{
  state = inputState;
  if (state == 'f')
  {
    direc = 1;
  }
  
  else if (state == 'r')
  {
    direc = -1;
  }
  
  else if (state == 's')
  {
    direc = 0;
  }


  if (state == 'c')
  {
    close_picker();
    
  }

  if (state == 'o')
  {
    open_picker();
  }
}
