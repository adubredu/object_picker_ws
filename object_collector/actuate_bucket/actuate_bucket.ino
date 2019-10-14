#include <Servo.h>
Servo servo;
const int angle = 180;
bool wasPressed = false;
bool isClosed = false;

void close_bucket()
{
  Serial.println("Closing Bucket");
  servo.writeMicroseconds(500);
  delay(3000);
}

void open_bucket()
{
   Serial.println("Opening Bucket");
   servo.writeMicroseconds(2500);
   delay(3000);

}

void setup() {
  pinMode(7, INPUT);
  Serial.begin(9600);
  servo.attach(5);
  servo.writeMicroseconds(1500);

}


void loop() 
{ 
  if (digitalRead(7) == HIGH)
  {
    Serial.println("Pressed");
      if (isClosed){
        open_bucket();
        isClosed = false;
      }
      else{
        close_bucket();
        isClosed = true;
      }
   
    wasPressed = true;
    
  }

  else{
    Serial.println("Not pressed");
    wasPressed = false;
    
  }

}
