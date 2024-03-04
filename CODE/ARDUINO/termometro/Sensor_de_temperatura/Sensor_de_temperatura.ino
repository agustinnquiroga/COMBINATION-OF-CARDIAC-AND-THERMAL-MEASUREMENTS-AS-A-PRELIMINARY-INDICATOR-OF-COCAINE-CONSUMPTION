// Declaracion de variables globales
float tempC; // Variable para almacenar el valor obtenido del sensor (0 a 1023)
int pinLM35 = 5; // Variable del pin de entrada del sensor (A5)

// Configuración funciones que corren solo una vez
void setup() {
  
  Serial.begin(9600); // Configuracion del puerto serial a 9600 bps 
}

// Funciones en loop
void loop() {
  
  tempC = analogRead(pinLM35); // Con analogRead lee el sensor
  tempC =  ((tempC*5/1024)/0.08); // Calcula la temperatura con la fórmula
  Serial.print(tempC); // Envia el dato al puerto serial
  Serial.print("\n"); // Salto de línea
  delay(1000); // Espera un tiempo para repetir el loop
}
















