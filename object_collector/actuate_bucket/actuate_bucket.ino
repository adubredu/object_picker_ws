#include <Servo.h>
Servo servo;
const int angle = 90;
bool wasPressed = false;
bool isClosed = false;

void close_bucket()
{
  Serial.println("Closing Bucket");
  servo.write(angle);
  delay(1000);
}

void open_bucket()
{
   Serial.println("Opening Bucket");
    servo.write(0);
    delay(1000);

}

void setup() {
  pinMode(7, INPUT);
  Serial.begin(9600);
  servo.attach(5);
  //servo.write(0);

}


void loop() 
{ 
  if (digitalRead(7) == HIGH)
  {
    Serial.println("Pressed");
    if (!wasPressed)
    {
      if (isClosed){
        open_bucket();
        isClosed = false;
      }
      else{
        close_bucket();
        isClosed = true;
      }
    }
    wasPressed = true;
    
  }

  else{
    Serial.println("Not pressed");
    wasPressed = false;
    
  }

}
