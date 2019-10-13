

#include <Servo.h>
Servo myservo;  
char user_input = 's';
char state = 's';
int n;
int direc=1; 
int INITPOS = 1000;
int MINPOS = 1000;
int MAXPOS = 1900;
int STEPSIZE = 10; 
String print_message;

void setup() {
  Serial.begin(9600);
  n = INITPOS;
  myservo.writeMicroseconds(n); 
  myservo.attach(9, MINPOS, MAXPOS); 
  setState('s');
}

void loop() 
{
  if (Serial.available())
  { 
        user_input = Serial.read();
      
      if (user_input != state)
        setState(user_input);
      
      if (n >= MINPOS and n <= MAXPOS) 
      {
          n = n + (direc * STEPSIZE);
          myservo.writeMicroseconds(n);
          if (n < MINPOS or n > MAXPOS) 
          {
            setState('s');
            if (n < MINPOS) 
              n = MINPOS;
            
            else 
              n = MAXPOS;
            
          }
          delay(100);
      }
  }

  else
  {
      direc = 0;
      n = n + (direc * STEPSIZE);
      myservo.writeMicroseconds(n);
  }
}

void setState(char inputState)
{
  state = inputState;
  if (state == 'f')
    direc = 1;
  
  else if (state == 'r')
    direc = -1;
  
  else if (state == 's')
    direc = 0;
  
}
