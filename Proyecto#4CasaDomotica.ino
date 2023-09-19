#include <Servo.h> // Librería del servo
Servo servo;
int servopin = 16; // Pin del servo
int angle = 0;    // Angulo inicial
#include "NewPing.h" // Librería del ultrasonido

// Primer ultrasonido puerta
#define TRIGGER_PIN1 9
#define ECHO_PIN1 10

// Segundo ultrasonido derecha
#define TRIGGER_PIN2 11
#define ECHO_PIN2 12

// Tercer ultrasonido izquierda
#define TRIGGER_PIN3 14
#define ECHO_PIN3 15

long duracion, distancia, puerta, izquierda, derecha; // Variables para mediciones de distancia

// Definición de pines de las luces
int izquierdaroja = 2;
int izquierdaverde = 3;
int derecharoja = 4; 
int derechaverde = 5; 
int luzadentro = 6;

int pResistor = A7; // Fotoresistencia

void setup() {
  Serial.begin(9600);
  // Luces izquierda
  pinMode(izquierdaroja, OUTPUT);
  pinMode(izquierdaverde, OUTPUT);
  digitalWrite(izquierdaroja, HIGH);
  digitalWrite(izquierdaverde, LOW);
  // Luces derecha
  pinMode(derecharoja, OUTPUT); // Agregué esta línea para configurar el pin de la luz derecha
  pinMode(derechaverde, OUTPUT); // Agregué esta línea para configurar el pin de la luz derecha
  // Luz adentro
  pinMode(luzadentro, OUTPUT); // Agregué esta línea para configurar el pin de la luz adentro
  // Fotoresistor
  pinMode(pResistor, INPUT);
  // Pines de los ultrasonidos
  pinMode(TRIGGER_PIN1, OUTPUT);
  pinMode(ECHO_PIN1, INPUT);
  pinMode(TRIGGER_PIN2, OUTPUT);
  pinMode(ECHO_PIN2, INPUT);
  pinMode(TRIGGER_PIN3, OUTPUT);
  pinMode(ECHO_PIN3, INPUT);
  // Setup del servo motor
  servo.attach(servopin);
  servo.write(angle);
}

// Función de medir distancia
void medir(int trigPin, int echoPin) {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duracion = pulseIn(echoPin, HIGH);
  distancia = (duracion) * 0.017;
}

// Función del fotoreceptor si la luz de adentro está apagada
void controlarLuzInterior() {
  int valorLuz = analogRead(pResistor); // Leer la luz con el fotoresistor
  Serial.println("LUZ=");
  Serial.print(valorLuz);
  Serial.println("\n");
  if (valorLuz > 400) {
    digitalWrite(luzadentro, LOW); // Apagar la luz interior si está oscuro
  } else {
    digitalWrite(luzadentro, HIGH); // Encender la luz interior si está claro
  }
}

void loop() {
  // Medir distancia en la puerta
  medir(TRIGGER_PIN1, ECHO_PIN1);
  puerta = distancia;
  // Medir distancia a la derecha de la casa
  medir(TRIGGER_PIN2, ECHO_PIN2);
  derecha = distancia;
  // Medir distancia a la izquierda de la puerta
  medir(TRIGGER_PIN3, ECHO_PIN3);
  izquierda = distancia;

  // Control de las luces izquierda
  if (izquierda < 15) 
  {
    digitalWrite(izquierdaroja, LOW);   // Apaga la luz roja izquierda
    digitalWrite(izquierdaverde, HIGH); // Enciende la luz verde izquierda
  } else 
  {
    digitalWrite(izquierdaroja, HIGH);  // Enciende la luz roja izquierda
    digitalWrite(izquierdaverde, LOW);  // Apaga la luz verde izquierda
  }

  // Control de las luces derecha
  if (derecha < 15) 
  {
    digitalWrite(derecharoja, LOW);    // Apaga la luz roja derecha
    digitalWrite(derechaverde, HIGH);  // Enciende la luz verde derecha
  } else 
  {
    digitalWrite(derecharoja, HIGH);   // Enciende la luz roja derecha
    digitalWrite(derechaverde, LOW);   // Apaga la luz verde derecha
  }

  // Control de la puerta
  if (puerta < 15) 
    {
      digitalWrite(luzadentro, HIGH);  // Enciende la luz adentro
      servo.write(angle + 90); // El servo se moverá 90 grados más de la posición inicial
                              // en nuestro caso, la posición inicial es 0
      delay(2000);
      servo.write(angle);  // El servo vuelve a su posición inicial cerrando la puerta
    }
  else 
    digitalWrite(luzadentro, LOW);   // Apaga la luz adentro

   // Este if verificará si la luz de adentro está apagada, en caso de estar apagada entonces
   // se realizará el control inteligente de luz 
  if (digitalRead(luzadentro == LOW)) {
    controlarLuzInterior();
  }
  
  delay(2000); // Un delay para que esté un poco más controlado, las mediciones se pueden cambiar
  // según queramos
}
