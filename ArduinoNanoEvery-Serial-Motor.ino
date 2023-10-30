#include <Servo.h>
Servo servo;
String nom = "Arduino";
String msg;
int ENA = 6;
int IN1 = 5;
int IN2 = 4;
int led = 13;
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
  readSerialPort();
}

void readSerialPort() {
  msg = "";
  if (Serial.available()) {
      delay(10);
      while (Serial.available() > 0) {
          msg += (char)Serial.read();
      }
      Serial.flush();
  }
}
