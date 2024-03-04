void setup() {
Serial.begin(9600);
}

void loop() {
  
int pulso; //variable donde se almacena el valor leído de el pin A0
pulso = analogRead(0); // lectura analógica del pin A0
Serial.println(pulso); // envía al serial plotter el valor leido
}
