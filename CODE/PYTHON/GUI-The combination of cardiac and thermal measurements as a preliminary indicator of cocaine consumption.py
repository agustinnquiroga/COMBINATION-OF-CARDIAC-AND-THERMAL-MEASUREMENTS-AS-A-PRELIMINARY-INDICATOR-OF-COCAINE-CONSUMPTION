import wx
import gettext
import threading
import serial
import cv2
import sys
import time
import numpy as np

#Hilo principal#        
class hilovalores(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.ser = serial.Serial('COM3', baudrate=9600)
        self.valorfc = []    #Variable donde se guardaran los valores al terminar el hilo
        self.valortc = []    #Variable donde se guardaran los valores al terminar el hilo
        self.segundos = 10    #Tiempo que tarda en levantar datos. 240 segundos = 4 minutos
        
    def run(self):
        tiempoinicial = time.time()
        limite = tiempoinicial + self.segundos
        while tiempoinicial<=limite: #Tiempo de espera hasta obtener los resultados
              tiempoinicial = time.time()
        while len(self.valorfc) <= 10: #Cantidad de valores que va a obtener antes de proseguir
            try: #No tiene en cuenta el error en descripto con except
                data = self.ser.readline().decode("utf-8") # utf-8 decodifica el byte como unicode (saca las /n/t)
                lista = data.split('\t') # Separa frecuencia cardíaca de temeperatura corporal
                self.valorfc.append( float(lista[0]) ) # Guarda en valorfc el valor de la frecuencia cardíaca
                self.valortc.append( float(lista[1]) ) # Guarda en valortc el valor de la temperatura corporal
                print(self.valorfc)
                print(self.valortc)
            except UnicodeDecodeError: # Error que no tiene en cuenta
                pass # Sigue ejecutando el programa
        self.valorfc = np.asarray(self.valorfc) # Arreglo de los valores
        self.valortc = np.asarray(self.valortc) # Arreglo de los valores
        self.fc=(np.median(self.valorfc)) # Guarda en fc el valor final de la mediana de la frecuencia cardíaca 
        self.tc=(np.median(self.valortc)+2) # Guarda en tc el valor final de la mediana de la temperatura corporal
        self.ser.close() #cierra puerto serie

#Interfaz gráfica#        
class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        wx.Frame.__init__(self, *args, **kwds)
        self.panel_1 = wx.Panel(self, wx.ID_ANY)
        self.label_timer = wx.StaticText(self.panel_1, wx.ID_ANY, _("05:00")) # Cronómetro
        self.label_result = wx.StaticText(self.panel_1, wx.ID_ANY, _("Coloque el termómetro y el dedo pulgar.\nLuego seleccione comenzar.")) # Mensaje 
        self.button_start = wx.Button(self.panel_1, wx.ID_ANY, _("Comenzar")) # Botón comenzar
        self.__set_properties()
        self.__do_layout()
        self.Bind(wx.EVT_BUTTON, self.button5_start_evt, self.button_start) # Al hacer click en "comenzar" empieza a funcionar el timer
        self.timer = wx.Timer(self, 10000)
        self.Bind(wx.EVT_TIMER, self.OnTimer)
        self.seconds = 0 # Segundos en que empieza el timer
        self.minutes = 5 # Minutos en que empieza el timer
        self.hilo1 = hilovalores() # Instancia el hilo
    
    #Timer interfaz gráfica#
    def OnTimer(self, event):
        self.label_result.SetLabel('Aguarde por favor...') # Mensaje al comenzar el cronómetro
        if self.seconds == 0:
            self.seconds = 59
            self.minutes = self.minutes - 1
        else:
            self.seconds = self.seconds - 1
        if (self.minutes == -1) and (self.seconds == 59):
            self.seconds = 0
            self.minutes = 0
            self.timer.Stop()
            
            #Según los valores finales de fc y tc muestra los mensajes indicados al terminar el timer
            if ( self.hilo1.fc > 110) and ( self.hilo1.tc > 38):
                    self.label_result.SetLabel('\nLa persona posee signos de estar bajos los efectos de la cocaína.\nSu frecuencia cardíaca es: {} LPM.\nSu temperatura corporal es: {} °C.'.format(self.hilo1.fc,self.hilo1.tc)) # Mensaje
            elif (self.hilo1.fc > 110) and (self.hilo1.tc < 38):
                    self.label_result.SetLabel('\nLa persona tiene frecuencia cardíaca alta.\nSu frecuencia cardíaca es: {} LPM.\nSu temperatura corporal es: {} °C.'.format(self.hilo1.fc,self.hilo1.tc)) # Mensaje
            elif (self.hilo1.fc < 110) and (self.hilo1.tc > 38):
                    self.label_result.SetLabel('\nLa persona tiene fiebre.\nSu frecuencia cardíaca es: {} LPM.\nSu temperatura corporal es: {} °C.'.format(self.hilo1.fc,self.hilo1.tc)) # Mensaje
            elif (self.hilo1.fc < 110) and (self.hilo1.tc < 38):
                    self.label_result.SetLabel('\nLa persona no posee signos de estar bajos los efectos de la cocaína.\nSu frecuencia cardíaca es: {} LPM.\nSu temperatura corporal es: {} °C.'.format(self.hilo1.fc,self.hilo1.tc)) # Mensaje
            else:
                    self.label_result.SetLabel('\nError de medición') # Mensaje    
        minutes = ''
        seconds = ''
        if self.seconds < 10:
            seconds = '0' + str(self.seconds)
        else:
            seconds = str(self.seconds)
        minutes =  '0' + str(self.minutes)
        self.label_timer.SetLabel(minutes + ':' + seconds)
    
    #Tamaño de la ventana#  
    def __set_properties(self):
        self.SetTitle(("Test de cocaína"))
        self.SetSize((1230, 400))
        self.label_timer.SetFont(wx.Font(80, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "")) #Caracterízticas de la fuente del cronómetro
        self.label_result.SetFont(wx.Font(30, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "")) #Caracterizticas de la fuente de los mensajes
        self.button_start.SetFont(wx.Font(22, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "")) #Caracterizticas de la fuente del botón
    #Diseño de la ventana#
    def __do_layout(self):
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_1 = wx.GridSizer(3, 1, 0, 0)
        grid_sizer_1.Add(self.label_timer, 0, wx.ALIGN_CENTER, 0)
        grid_sizer_1.Add(self.label_result, 0, wx.ALL, 5)
        grid_sizer_1.Add(self.button_start, 0, wx.ALIGN_BOTTOM | wx.ALIGN_RIGHT | wx.ALL, 5)
        sizer_2.Add(grid_sizer_1, 1, wx.EXPAND, 0)
        self.panel_1.SetSizer(sizer_2)
        sizer_1.Add(self.panel_1, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        self.Layout()
        
    #Acciones al hacer click en "comenzar"#
    def button5_start_evt(self, event):
        self.timer.Start(1000)
        self.hilo1.start() # Inicia el hilo 
        event.Skip()

#Abre la ventana al iniciar el programa#
class MyApp(wx.App):
    def OnInit(self):
        frame_1 = MyFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(frame_1)
        frame_1.Show()
        return True

if __name__ == "__main__":
    gettext.install("app") 
    app = MyApp(0)
    app.MainLoop()