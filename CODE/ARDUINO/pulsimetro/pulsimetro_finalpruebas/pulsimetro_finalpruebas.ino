#include "ThresholdLib.h"
#include "MedianFilterLib.h"

Threshold<int> threshold(500, 100); // Valores umbralizadores, (1,0)
MedianFilter<int> medianFilter(5); // Único parametro de la función que calcula la mediana, toma (x) valores

//Variables para medir el tiempo entre muestra y muestra
 unsigned long pasado = 0; 
 unsigned long ahora ;
 unsigned long tiempo;
 unsigned long diferencialtiempo;
 unsigned long diferencialpulso;
 
 unsigned long pulso; //variable donde se almacena el valor leído de el pin A0
 int derivada; // Variable donde se guarda la señal derivada
 unsigned long umbralizadapasada = 0; // Variable donde se guarda la señal umbralizada

 // Variables utilizadas para medir el tiempo entre pulso y pulso
 unsigned long fc; // Variable donde se guarda el valor de frecuencia cardíaca
 unsigned long tiemposegundo;
 unsigned long tiempoprimero = 0;
 unsigned long tiempopulso;

// Configuración funciones que corren solo una vez
void setup() 
{
  Serial.begin(9600);// Configuracion del puerto serial a 9600 bps 
}
// Funciones en loop
void loop() 
{
   unsigned long tiempo=micros(); //variables para medir el tiempo entre muestra y muestra, micros() cuenta en microsegundos;
 
 
    pulso = analogRead(0); // lectura analógica del pin A0
    Serial.println(pulso);

 // Calcular filtro
    bool umbralizada = threshold.AddValue(pulso); //Función de la librería para umbralizar 
    
 // Mostrar resultados   
    // Serial.println(pulso); //Grafica el pulso como llega a arduino
    // Serial.println(umbralizada * 500);  //Grafica la señal umbralizada

 // Derivación

    ahora= tiempo;
    diferencialtiempo = ahora - pasado ;
    diferencialpulso= umbralizada - umbralizadapasada ;
    derivada = (diferencialpulso/diferencialtiempo) ;
    umbralizadapasada=umbralizada;
    pasado = ahora;
    
 // Mostrar derivada    
    //Serial.println(derivada);

 // Calculo de FC
 
    if (derivada > 0){ 
      tiemposegundo = ahora;
      tiempopulso = tiemposegundo - tiempoprimero;
      
      if ((tiempopulso < 1200000) && (tiempopulso > 300000)){
        //if (tiempopulso > 272727){
          
          fc= 60000000/tiempopulso;
 
          // Calcular mediana movil
          
            int mean = medianFilter.AddValue(fc);; //calcula mediana

          // Mostrar resultados
            //Serial.print(fc);
            //Serial.print("\t");
            //Serial.println(mean);

             //}    
      }
      tiempoprimero = tiemposegundo; 
    }      
}
