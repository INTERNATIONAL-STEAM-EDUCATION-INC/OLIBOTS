#include <Servo.h>
Servo servo;
String nom = "Arduino";
String msg;
int ENA = 9;
int IN1 = 7;
int IN2 = 6;
int ledROJO = 13;
int ledVERDE = 14;

void setup(){
  Serial.begin(9600);
  pinMode(ledROJO, OUTPUT);
  pinMode(ledVERDE, OUTPUT);  
  pinMode(ENA, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  servo.attach(5);
  servo.write(95);
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
}

void loop(){
  readSerialPort();
  Serial.println(msg);
  //analogWrite(ENA, 130);
  //servo.write(90);
  
  while (msg.equals("rojo")){
    // instrucciones para rojo
    digitalWrite(ledROJO, HIGH);
    analogWrite(ENA, 130);
    servo.write(135);
    readSerialPort();
  }
  while (msg.equals("verde")){
    // instrucciones para verde
    digitalWrite(ledVERDE, HIGH);
    analogWrite(ENA, 255);
    servo.write(55);
    readSerialPort();
  }
  while (msg.equals("siga")){
    // instrucciones para siga
    digitalWrite(ledROJO, LOW);
    digitalWrite(ledVERDE, LOW);
    analogWrite(ENA, 180);
    servo.write(95);
    readSerialPort();
  }
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