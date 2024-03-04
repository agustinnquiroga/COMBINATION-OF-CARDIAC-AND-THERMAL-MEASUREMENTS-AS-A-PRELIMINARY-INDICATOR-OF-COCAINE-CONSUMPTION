#include "ThresholdLib.h"
#include "MedianFilterLib.h"

Threshold<int> threshold(500, 100); 
MedianFilter<int> medianFilter(5); 

 unsigned long pasado = 0; 
 unsigned long ahora ;
 unsigned long tiempo;
 unsigned long diferencialtiempo;
 unsigned long diferencialpulso;
 unsigned long pulso; 
 int derivada;
 unsigned long umbralizadapasada = 0;
 unsigned long fc;
 unsigned long tiemposegundo;
 unsigned long tiempoprimero = 0;
 unsigned long tiempopulso;
 float tempC;
 int pinLM35 = 5;
 
void setup() 
{
  Serial.begin(9600);
}
void loop() 
{
   unsigned long tiempo=micros(); 
 
    pulso = analogRead(0); 
    tempC = analogRead(pinLM35);

    tempC =  ((tempC*5/1024)/0.08);
    
    bool umbralizada = threshold.AddValue(pulso);
    
    ahora= tiempo;
    diferencialtiempo = ahora - pasado ;
    diferencialpulso= umbralizada - umbralizadapasada ;
    derivada = (diferencialpulso/diferencialtiempo) ;
    umbralizadapasada=umbralizada;
    pasado = ahora;
    
    if (derivada > 0){ 
      tiemposegundo = ahora;
      tiempopulso = tiemposegundo - tiempoprimero;
      
      if ((tiempopulso < 1200000) && (tiempopulso > 300000)){
          
          fc= 60000000/tiempopulso;
   
            int mean = medianFilter.AddValue(fc);; //calcula mediana

            
            Serial.print(mean);
            Serial.print("\t");
            Serial.println(tempC);
      }
      tiempoprimero = tiemposegundo; 
    }      
}
