# -*- coding: utf-8 -*-
"""
Created on Tue Jul 31 20:09:56 2018

@author: lenovo
"""
import wx
import threading
import serial
import cv2
import sys
import time
import numpy as np

        
class hilovalores(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.ser = serial.Serial('COM3', baudrate=9600)
        self.valorfc = []    #Variable donde se guardaran los valores al terminar el hilo
        self.valortc = []    #Variable donde se guardaran los valores al terminar el hilo
        self.segundos = 3    #240 segundos = 4 minutos
        
    print('\nPor favor aguarde 5 minutos')   # Le indica a la persona que espere
    def run(self):
        tiempoinicial = time.time()
        limite = tiempoinicial + self.segundos
        while tiempoinicial<=limite: #tiempo de espera hasta obtener los resultados si el tiempo es 4 minutos colocar menos tiempo para que tome los valores anteriores al termino
              tiempoinicial = time.time()
        
        while len(self.valorfc) <= 4: #Cantidad de valores que va a obtener antes de proseguir
            try: #No tiene en cuenta el error en descripto con except
                data = self.ser.readline().decode("utf-8") # utf-8 decodifica el byte como unicode (saca las /n/t)
                lista = data.split('\t') # Separa frecuencia cardíaca de temeperatura corporal
                self.valorfc.append( float(lista[0]) ) # Guarda en valorfc el valor de la frecuencia cardíaca
                self.valortc.append( float(lista[1]) ) # Guarda en valortc el valor de la temperatura corporal
            except UnicodeDecodeError: # Error que no tiene en cuenta
                pass # Sigue ejecutando el programa
        
        self.valorfc = np.asarray(self.valorfc) # Arreglo de los valores
        self.valortc = np.asarray(self.valortc) # Arreglo de los valores
        self.fc=(np.median(self.valorfc)) # Guarda en fc el valor final de la mediana de la frecuencia cardíaca 
        self.tc=(np.median(self.valortc)) # Guarda en tc el valor final de la mediana de la temperatura corporal
        self.ser.close() #cierra puerto serie
        if ( self.fc > 110) and ( self.tc > 38):
            print('\nEl sujeto posee signos de estar bajos los efectos de la cocaína')
            print('\nFrecuencia cardíaca: {}.'.format(self.fc)) # Muestra valor de frecuencia cardíaca
            print('\nTemperatura corporal:{}'.format(self.tc)) # Muesra valor de temperatura corporal
        elif (self.fc>110) and (self.tc<38):
            print('\nEl sujeto tiene frecuencia cardíaca alta')
            print('\nFrecuencia cardíaca: {}.'.format(self.fc)) # Muestra valor de frecuencia cardíaca
            print('\nTemperatura corporal:{}'.format(self.tc)) # Muesra valor de temperatura corporal
        elif (self.fc<110) and (self.tc>38):
            print('\nEl sujeto tiene fiebre')
            print('\nFrecuencia cardíaca: {}.'.format(self.fc)) # Muestra valor de frecuencia cardíaca
            print('\nTemperatura corporal:{}'.format(self.tc)) # Muesra valor de temperatura corporal
        elif (self.fc<110) and (self.tc<38):
            print('\nEl sujeto no posee signos de estar bajos los efectos de la cocaína')
            print('\nFrecuencia cardíaca: {}.'.format(self.fc)) # Muestra valor de frecuencia cardíaca
            print('\nTemperatura corporal:{}'.format(self.tc)) # Muesra valor de temperatura corporal
        else:
            print('\nError de medición')
 
hilo1 = hilovalores()
hilo1.start()

    

