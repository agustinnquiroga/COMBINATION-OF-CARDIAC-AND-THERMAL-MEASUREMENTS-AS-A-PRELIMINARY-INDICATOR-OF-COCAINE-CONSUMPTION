#include "ThresholdLib.h"

Threshold<int> threshold(599, 200); // Valores umbralizadores, (1,0)

void setup() 
{
  Serial.begin(9600);
 
}

void loop() 
{
 int pulso; //variable donde se almacena el valor leído de el pin A0
 pulso = analogRead(0); // lectura analógica del pin A0

    // Calcular filtro
    bool state = threshold.AddValue(pulso); //Función de la librería para umbralizar 

////////// Mostrar resultados
    
    //Serial.println(pulso); //Grafica el pulso como llega a arduino
    Serial.println(state * 500);  //Grafica la señal umbralizada
  
}
