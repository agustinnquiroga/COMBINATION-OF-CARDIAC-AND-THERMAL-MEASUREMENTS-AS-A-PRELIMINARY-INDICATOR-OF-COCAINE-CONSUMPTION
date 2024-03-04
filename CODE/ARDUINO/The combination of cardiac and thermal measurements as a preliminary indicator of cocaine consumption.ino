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

 //Variables sensor de temperatura
 float tempC; // Variable para almacenar el valor obtenido del sensor (0 a 1023)
 int pinLM35 = 5; // Variable del pin de entrada del sensor (A5)

// Configuración funciones que corren solo una vez
void setup() 
{
  Serial.begin(9600);// Configuracion del puerto serial a 9600 bps 
}

// Funciones en loop
void loop() 
{
   unsigned long tiempo=micros(); //variables para medir el tiempo entre muestra y muestra, micros() cuenta en microsegundos
    pulso = analogRead(0); // lectura analógica del pin A0
    tempC = analogRead(pinLM35); // Con analogRead lee el sensor
    tempC =  ((tempC*5/1024)/0.08); // Calcula la temperatura con la fórmula

    // Umbralización de señal
    bool umbralizada = threshold.AddValue(pulso); //Función de la librería para umbralizar 
    
    // Derivación de señal
    ahora= tiempo; //El tiempo se guarda en ahora
    diferencialtiempo = ahora - pasado ; //Cálculo del diferencial del tiempo
    diferencialpulso= umbralizada - umbralizadapasada ; //Cálculo diferencial del pulso
    derivada = (diferencialpulso/diferencialtiempo) ; //Cálculo derivada
    umbralizadapasada=umbralizada; //El valor actual de la señal se guarda para en el próximo loop utilizarlo
    pasado = ahora; //El valor acutal del tiempo se guarda para, en el próximo loop, utilizarlo
    
    // Calculo de FC
    if (derivada > 0){ //Condición de que la señal derivada sea mayor a 0 (se produjo un pulso)
      tiemposegundo = ahora; // El tiempo se guarda en tiemposegundo
      tiempopulso = tiemposegundo - tiempoprimero; // Se calcúla el tiempo transcurrido entre pulso y pulso (FC instantanea)
      
    // Filtro para eliminar ruido
      if ((tiempopulso < 1200000) && (tiempopulso > 300000)){ //Elimina valores de frecuencia cardíaca por debajo de 50 y por arriba a 200
        fc= 60000000/tiempopulso; //Calcula el valor de la FC
   
    // Calcular mediana movil
         int mean = medianFilter.AddValue(fc);; //Calcula la mediana

    // Imprimeresultados
            Serial.print(mean); //Frecuencia cardíaca 
            Serial.print("\t"); //Espacio
            Serial.println(tempC);//Temperatura corporal
      }
      tiempoprimero = tiemposegundo; //El valor del tiempo acutal del pulso se guarda para, en el próximo loop utilizarlo
    }      
}
