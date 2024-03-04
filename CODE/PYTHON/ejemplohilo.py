# -*- coding: utf-8 -*-
"""
Created on Tue Aug 14 11:29:56 2018

@author: lenovo
"""
import threading, time

vmax_hilos = {}

def contar(segundos):
    """Contar hasta un límite de tiempo"""
    global vmax_hilos
    contador = 0
    inicial = time.time()
    limite = inicial + segundos
    nombre = threading.current_thread().getName()
    while inicial<=limite:
        contador+=1
        inicial = time.time()
        print(nombre, contador)
    
    vmax_hilos[nombre] = contador
    if threading.active_count()==2:
        print(vmax_hilos)
        print(threading.enumerate())

segundos = 1
for num_hilo in range(5):
    hilo = threading.Thread(name='hilo%s' %num_hilo,
                            target=contar, 
                            args=(segundos,))
    hilo.start()