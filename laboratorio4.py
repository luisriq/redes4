# -*- coding: utf-8 -*-
import numpy as np
from scipy.io.wavfile import read, write
import matplotlib.pyplot as plt
import matplotlib
import math
from scipy.fftpack import fft, fftfreq, ifft
from scipy.signal import *
from scipy import integrate
x0 = 0.002
largo = 0.005
limitesx = (x0, x0+largo)

def fir_filter_lp(data, rate, cutoff_hz, numtaps): #funcion que calcula el filtro FIR con lowpass
	nyquist_rate = rate / 2.    #Nyquist rate
	fir_coeff = firwin(numtaps, cutoff_hz/nyquist_rate)  #crea el filtro FIR lowpass
	filtered_signal_freq = np.convolve(data, fir_coeff, 'same')

	return filtered_signal_freq

def graficoTiempo(datos, rate, p):
	ar_tiempo = np.linspace(0, len(datos)/rate, len(datos))
	p.plot(ar_tiempo, (datos), 'r')
	p.set_xlim(limitesx[0], limitesx[1])
	p.set_title("Señal Original")

def graficoAM(datos, rate,nuevorate, p, st = False, demod = False):
	w0 =  np.pi*nuevorate/8
	segs = len(datos)/rate
	newlen = nuevorate*len(datos)/rate
	datos = resample(datos, newlen)
	carrier = np.cos(w0*np.linspace(0., float(segs), newlen ))
	ar_tiempo = np.linspace(0, len(datos)/nuevorate, len(datos))
	datosAM = datos*carrier
	p.set_title("Señal AM")
	if(demod):
		datosAM = fir_filter_lp(datosAM,nuevorate,4096,1000)
		p.set_title("Señal Demodularizada")
	if(st):
		transformada = fft(datosAM)
		freq = fftfreq(transformada.size, 1/rate)
		p.plot(freq, transformada, 'r')
		return
	p.plot(ar_tiempo, (datosAM), 'g')
	p.set_xlim(limitesx[0], limitesx[1])
	return (datosAM,carrier)
def graficoFM(datos, rate,nuevorate,k, p, st = False, demod = False):
	w0 =  np.pi*nuevorate/32
	segs = len(datos)/rate
	newlen = nuevorate*len(datos)/rate
	datos = resample(datos, newlen)
	ar_tiempo = np.linspace(0, len(datos)/nuevorate, newlen)
	a = w0*np.linspace(0., float(segs), newlen )

	b = integrate.cumtrapz(datos, ar_tiempo, initial = 0)
	datosAM = np.cos(a+k*b)
	p.set_title("Señal FM")
	if(demod):
		datosAM = fir_filter_lp(datosAM,nuevorate,4096,1000)
		p.set_title("Señal Demodularizada")
	if(st):
		transformada = fft(datosAM)
		freq = fftfreq(transformada.size, 1/rate)
		p.plot(freq, transformada, 'r')
		return
	p.plot(ar_tiempo, 8000*(datosAM), 'g')
	p.set_xlim(limitesx[0], limitesx[1])
	return (datosAM,carrier)
	
	
#Leyendo el archivo
rate,info = read('handel.wav')
f, plots = plt.subplots(2)
info = info[:rate]
f.subplots_adjust( hspace=0.7 )
print(rate)
graficoTiempo(info, rate, plots[0]) 
datosAM,carrier = graficoAM(info, rate,200000, plots[0])
#graficoAM(datosAM, 200000,200000, plots[2], st=False, demod=True)
graficoFM(info, rate,2000000,50, plots[1])
graficoTiempo(info, rate, plots[1]) 

f.show()
input("Presione enter para salir:\n")
	

