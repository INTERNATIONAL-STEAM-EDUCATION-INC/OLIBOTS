#include <Servo.h>
Servo servo;
String nom = "Arduino";
String msg;
int ENA = 6;
int IN1 = 5;
int IN2 = 4;
int led = 13;
void setup(){
  Serial.begin(115200);
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
  Serial.println(msg);
  if (msg.equals("rojo")){
    // instrucciones para rojo
  }
  if (msg.equals("verde")){
    // instrucciones para verde
  }
  if (msg.equals("siga")){
    // instrucciones para siga
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
