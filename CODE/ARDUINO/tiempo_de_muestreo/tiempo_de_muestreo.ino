void setup(){

  Serial.begin(9600);
  muestreo();

}

void loop(){
}

void muestreo(){

  unsigned long time1=0;
  unsigned long time=0;
  Serial.println("*************************");
  Serial.println("ENSAYO TIEMPO DE MUESTRO:");
  Serial.println("*************************");
  for(byte i =0; i<4; i++){
    time1=micros();
    int A=analogRead(A0);
    time=micros()-time1;
    Serial.print(" Muestra: ");
    Serial.print(i+1);
    Serial.print(" Tiempo: ");
    Serial.println(time);
  }

}
