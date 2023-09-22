#include <Servo.h>
Servo servo;
int option;
int ENA = 6;
int IN1 = 5;
int IN2 = 4;
void setup(){
  Serial.begin(9600);
  pinMode(led, OUTPUT); 
  pinMode(ENA, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  servo.attach(3);
}

void loop(){
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  analogWrite(ENA, 255);
  servo.write(90);
  if (Serial.available()>0){
    option=Serial.read();
    if(option=='a') {
      servo.write(30);
      delay(500);
    }
    if(option=='b') {
      servo.write(150);
      delay(500);
    }
  }
}
