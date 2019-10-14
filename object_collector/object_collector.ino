#include <Servo.h>
Servo servo;

void sweep_object()
{
   for (int i=60; i>=0; i--)
   {
    servo.write(i);
    delay(10);
   }
  delay(2000);
  for (int i=0; i<=60; i++)
   {
    servo.write(i);
    delay(10);
   }
   


   
  
//   servo.write(5);
}


void setup() {
  pinMode(7, INPUT);
  Serial.begin(9600);

  servo.attach(5);
  servo.write(0);

}


void loop() 
{
  if (digitalRead(7) == HIGH)
  {
    Serial.println("Pressed");
    sweep_object();
  }

  else
    Serial.println("Not pressed");

}
