
#include <ax12.h>
const int panID = 1;
const int tiltID = 2;
const int tilt_home = 515;
const int pan_home = 500; 
int pan_angle = pan_home;
int tilt_angle = tilt_home;

int delta = 20;

void setup() {
  Serial.begin(9600);
  dxlSetGoalPosition(tiltID, tilt_angle);
  dxlSetGoalPosition(panID, pan_angle);
}

void loop() {
  while (Serial.available() > 0)
  {
    char input = Serial.read();
    interprete_input(input);
  }
}

void turn_left()
{
    if (pan_angle < 1000){
      int target = pan_angle + delta;
      while (pan_angle < target)
      {
        pan_angle += 5;
        dxlSetGoalPosition(panID, pan_angle);
        delay(100);
      }
      
    }
}

void turn_right()
{
    if (pan_angle > 20){
      int target = pan_angle - delta;
      while (pan_angle > target)
      {
        pan_angle -= 5;
        dxlSetGoalPosition(panID, pan_angle);
        delay(100);
      }
    }
}

void tilt_up()
{
    if (tilt_angle < 830)
    {
      int target = tilt_angle + delta;
      while (tilt_angle < target)
      {
        tilt_angle += 5;
        dxlSetGoalPosition(tiltID, tilt_angle);
        delay(100);
      }
    }
}

void tilt_down()
{
    if (tilt_angle > 210)
    {
      int target = tilt_angle - delta;
      while (tilt_angle > target)
      {
        tilt_angle -= 5;
        dxlSetGoalPosition(tiltID, tilt_angle);
        delay(100);
      }
    }
}

void center()
{
  while (abs(tilt_angle - tilt_home)>20 or abs(pan_angle - pan_home)>20)
  {
    if ((tilt_angle - tilt_home) < -20)
      tilt_up();

    else if ((tilt_angle - tilt_home) > 20)
      tilt_down();

    if ((pan_angle - pan_home) < -20)
      turn_left();

    else if ((pan_angle - pan_home) > 20)
      turn_right(); 
    
  }
}

int get_servo_position(int servoID){
  int position;
  for(int i = 0; i < 10; i++){
    position = dxlGetPosition(servoID);
    if(position > -1){
      return position;
    }
  }
  Serial.print("Failed reading position of servo ");
  Serial.println(servoID);
  return -1;
}

void display_servo_position(int servoID){
    Serial.print("Servo ");
    Serial.print(servoID);
    Serial.print(" at position ");
    Serial.println(get_servo_position(servoID));
}

void interprete_input(char input)
{
  switch (input)
  {
    case 'l':
      turn_left();
      break;
      
    case 'r':
      turn_right();
      break;

    case 'u':
      tilt_up();
      break;

    case 'd':
      tilt_down();
      break;

    case 'h':
      center();
      break;

    case 'w':
      display_servo_position(panID);
      display_servo_position(tiltID);
      break;
      
    default:
      return;
  }
}
