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
  servo.write(90);
}

void loop(){
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  readSerialPort();
  Serial.println(msg);
  analogWrite(ENA, 130);
  //servo.write(90);
  while (msg.equals("rojo")){
    // instrucciones para rojo
    digitalWrite(ledROJO, HIGH);
    //digitalWrite(ENA, LOW);
    analogWrite(ENA, 32);
    servo.write(130);
    //delay(50);
    readSerialPort();
    digitalWrite(ledROJO, LOW);
    delay(200);

  }
  while (msg.equals("verde")){
    // instrucciones para verde
    digitalWrite(ledVERDE, HIGH);
    //digitalWrite(ENA, LOW);
    analogWrite(ENA, 255);
    servo.write(50);
    //delay(50);
    readSerialPort();
    digitalWrite(ledVERDE, LOW);
    delay(200);
  }
  while (msg.equals("siga")){
    // instrucciones para siga
    digitalWrite(ledROJO, LOW);
    digitalWrite(ledVERDE, LOW);
    analogWrite(ENA, 255);
    servo.write(90);
    //delay(50);
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
