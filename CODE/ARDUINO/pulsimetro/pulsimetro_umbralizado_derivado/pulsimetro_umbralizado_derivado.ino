#include "ThresholdLib.h"

Threshold<int> threshold(599, 10); // Valores umbralizadores, (1,0)

 unsigned long pasado = 0; //variables para medir el tiempo entre muestra y muestra
 unsigned long ahora ;
 unsigned long tiempo;
 unsigned long diferencialtiempo;
 unsigned long diferencialpulso;
 unsigned long pulso; //variable donde se almacena el valor leído de el pin A0
 int derivada;
 int y = 0;
 unsigned long umbralizadapasada = 0;
 unsigned long fc;
 unsigned long tiemposegundo;
 unsigned long tiempoprimero = 0;
 unsigned long tiempopulso;
 //Si las variables se declaran como float se constata la parte negativa de lla derivada
 
 //float diferencialpulso;
 //float pulso; //variable donde se almacena el valor leído de el pin A0
 //float derivada;
 //float umbralizadapasada;

void setup() 
{
  Serial.begin(9600);
}
void loop() 
{
   unsigned long tiempo=micros(); //variables para medir el tiempo entre muestra y muestra millis() funcion que cuenta en milisegundos;
 
 
 // lectura analógica del pin A0
    pulso = analogRead(0); 

 // Calcular filtro
    bool umbralizada = threshold.AddValue(pulso); //Función de la librería para umbralizar 
    
 // Mostrar resultados   
    //Serial.println(pulso); //Grafica el pulso como llega a arduino
    //Serial.println(umbralizada * 500);  //Grafica la señal umbralizada

 // Derivación

    ahora= tiempo;
    diferencialtiempo = ahora - pasado ;
    diferencialpulso= umbralizada - umbralizadapasada ;
    
    //Serial.println(ahora);
    //Serial.println(diferencialtiempo);
    
    derivada = (diferencialpulso/diferencialtiempo) ;
    umbralizadapasada=umbralizada;
    pasado = ahora;
    
    //fc=derivada*3/50000 ;
    //Serial.println(derivada);


    if (derivada > 0){
      
      tiemposegundo = ahora;
      tiempopulso = tiemposegundo - tiempoprimero;
      
      if (tiempopulso < 1200000){
        fc= 60000000/tiempopulso;
        media= fc
        Serial.println(fc);
      }
      //Serial.println(tiemposegundo);
      //Serial.println(tiempoprimero);
      tiempoprimero = tiemposegundo; 
    }
      
}
