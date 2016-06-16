# -*- coding: utf-8 -*-
import numpy as np
from scipy.io.wavfile import read, write
import matplotlib.pyplot as plt
import matplotlib
import math
from scipy.fftpack import fft, fftfreq, ifft
from scipy.signal import *

def graficoTiempo(datos, rate, p):
	ar_tiempo = np.linspace(0, len(datos)/rate, len(datos))
	p.plot(ar_tiempo, (datos), 'g')

def graficoAM(datos, rate, p):
	w0 = np.pi
	segs = len(datos)/rate
	print("minmax(%f, %f)"%(0,segs))
	carrier = np.cos(9*np.pi*np.linspace(0., float(segs), len(datos)))
	print(carrier[rate-(rate/2):rate])
	ar_tiempo = np.linspace(0, len(datos)/rate, len(datos))
	print("len:(%d,%d)"%(len(carrier),len(datos)))
	datosAM = np.multiply(datos, carrier)
	#p.plot(ar_tiempo, (datosAM), 'g')
	p.plot(ar_tiempo, carrier, 'r')



#Leyendo el archivo
rate,info = read('handel.wav')
f, plots = plt.subplots(2)

f.subplots_adjust( hspace=0.7 )

graficoTiempo(info, rate, plots[0])
graficoAM(info, rate, plots[1])

f.show()

input("Presione enter para salir:\n")
