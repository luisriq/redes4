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
largo = 0.002
limitesx = (x0, x0+largo)

def fir_filter_lp(data, rate, cutoff_hz, numtaps): #funcion que calcula el filtro FIR con lowpass
	nyquist_rate = rate / 2.    #Nyquist rate
	fir_coeff = firwin(numtaps, cutoff_hz/nyquist_rate)  #crea el filtro FIR lowpass
	filtered_signal_freq = np.convolve(data, fir_coeff, 'same')
	return filtered_signal_freq

def graficoFrecuencia(datos,rate, p, titulo = ""):
	transformada = fft(datos)
	freq = fftfreq(transformada.size, 1/rate)
	p.plot(freq, transformada, 'r')
	p.set_title(titulo)
def graficoTiempo(datos, rate, p, color='r'):
	ar_tiempo = np.linspace(0, len(datos)/rate, len(datos))
	p.plot(ar_tiempo, (datos), color)
	p.set_xlim(limitesx[0], limitesx[1])

def graficoAM(datos, rate,nuevorate, p, st = False, demod = False, pm = 1, color = 'g', titulo=''):
	w0 =  np.pi*nuevorate/4
	segs = len(datos)/rate
	newlen = nuevorate*len(datos)/rate
	datos = resample(datos, newlen)

	carrier = np.cos(w0*np.linspace(0., float(segs), newlen ))
	ar_tiempo = np.linspace(0, len(datos)/nuevorate, len(datos))
	#A = (np.max(datos)/pm)
	Vm = np.max(datos)-np.min(datos)
	Vc =  np.max(carrier)-np.min(carrier)
	M = Vm/Vc
	A = pm/M
	# 
	#print(A)
	datosAM = A*datos*carrier
	p.set_title(titulo)
	if(demod):
		datosAM = fir_filter_lp(datosAM,nuevorate,4096,1000)
		p.set_title("Señal Demodularizada")
	if(st):
		transformada = fft(datosAM)
		freq = fftfreq(transformada.size, 1/nuevorate)
		p.plot(freq, transformada, 'r')
		return
	p.plot(ar_tiempo, (datosAM), color)
	p.set_xlim(limitesx[0], limitesx[1])
	return (datosAM,carrier)

def graficoFM(datos, rate,nuevorate,k, p, st = False, titulo=""):
	w0 =  np.pi*nuevorate/32
	segs = len(datos)/rate
	newlen = nuevorate*len(datos)/rate
	datos = resample(datos, newlen)
	ar_tiempo = np.linspace(0, len(datos)/nuevorate, newlen)
	a = w0*np.linspace(0., float(segs), newlen )

	b = integrate.cumtrapz(datos, ar_tiempo, initial = 0)
	
	datosAM = np.cos(a+k*b)
	p.set_title(titulo)
	if(st):
		transformada = fft(datosAM)
		freq = fftfreq(transformada.size, 1/rate)
		p.plot(freq, transformada, 'r')
		return
	p.plot(ar_tiempo, 8000*(datosAM), 'g')
	p.set_xlim(limitesx[0], limitesx[1])
	return datosAM

def modulacionDigital(datos, rate):
	pass



#Leyendo el archivo
rate,info = read('handel.wav')

f, plots = plt.subplots(3)
f.suptitle("Modulación")
plots[0].grid(True)
plots[1].grid(True)
plots[2].grid(True)
info = info[:rate]
f.subplots_adjust( hspace=1 )

# Parte 1.a
# Grafico tiempo normalizado (?)
graficoTiempo(info/np.max(info), rate, plots[0])
# Grafico AM
datosAM,carrier = graficoAM(info, rate,200000, plots[0], pm=1.0, color='c', titulo = 'Señal AM')
# Grafico modulado FM
graficoFM(info, rate,2000000,50, plots[1], titulo = "Señal FM")
graficoTiempo(info, rate, plots[1]) 
#plots[0].legend(handles=[l_signal,l_signal_rc_25,l_signal_rc_5,l_signal_rc_75,l_signal_rc_1],prop={'size':10})

# Grafico señal demodularizada AM
graficoAM(datosAM, 200000,200000, plots[2], st=False, demod=True, color='g')
# Comparando con señal original
graficoTiempo(info/np.max(info), rate, plots[2])
# Frecuencia
#graficoAM(info, rate,200000, plots[3], pm=1.0, color='c', titulo = 'Señal AM', st = True)
#graficoFM(info, rate,2000000,50, plots[1], titulo = "Señal FM", st = True)

f.show()
f.savefig("figura1a.eps")
input("Presione enter para seguir:\n")
# Parte 1.b

f, plots = plt.subplots(4)
f.subplots_adjust( hspace=1 )

#graficoFM(info, rate,2000000,50, plots[2], False)

graficoAM(info, rate,200000, plots[0], pm=0.25, color = 'r', titulo = 'Señal AM')
graficoAM(info, rate,200000, plots[0], pm=1.5, color = 'g', titulo = 'Señal AM')
graficoAM(info, rate,200000, plots[0], pm=2.75, color = 'b', titulo = 'Señal AM')

graficoFrecuencia(info, rate, plots[1], titulo = "Frecuencia Original")
graficoAM(info, rate,200000, plots[2], pm=1.0, st = True,color = 'r', titulo = 'Frecuencia Señal AM')
graficoFM(info, rate,2000000,50, plots[3], titulo = "Frecuencia Señal FM", st = True)
#graficoTiempo(info, rate, plots[2]) 

f.show()
f.savefig("figura1b.eps")
input("Presione enter para salir:\n")
