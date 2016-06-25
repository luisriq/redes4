# -*- coding: utf-8 -*-
import numpy as np
from scipy.io.wavfile import read, write
import matplotlib.pyplot as plt
import matplotlib
import math
from scipy.fftpack import fft, fftfreq, ifft
from scipy.signal import *
from scipy import integrate
import matplotlib.patches as mpatches
x0 = 0.001
largo = 0.003
limitesx = (x0, x0+largo)

# Filtro low pass para demodularizar AM
def fir_filter_lp(data, rate, cutoff_hz, numtaps): #funcion que calcula el filtro FIR con lowpass
	nyquist_rate = rate / 2.    #Nyquist rate
	fir_coeff = firwin(numtaps, cutoff_hz/nyquist_rate)  #crea el filtro FIR lowpass
	filtered_signal_freq = np.convolve(data, fir_coeff, 'same')
	return filtered_signal_freq

# Graficar espectro de frecuencias
def graficoFrecuencia(datos,rate, p, titulo = ""):
	transformada = fft(datos)
	freq = fftfreq(transformada.size, 1/rate)
	p.plot(freq, transformada, 'r')
	p.set_title(titulo)
# Grafico simple de la señal en el tiempo
def graficoTiempo(datos, rate, p, color='r'):
	ar_tiempo = np.linspace(0, len(datos)/rate, len(datos))
	p.plot(ar_tiempo, (datos), color)
	p.set_xlim(limitesx[0], limitesx[1])
# Grafico AM con porcentaje de modulacion
def graficoAMMod(datos, rate,nuevorate, p, st = False, demod = False, pm = 1, color = 'g', titulo=''):
	pm = 10*pm
	w0 =  np.pi*nuevorate/4
	segs = len(datos)/rate
	newlen = nuevorate*len(datos)/rate

	datos = resample(datos, newlen)

	carrier = np.cos(w0*np.linspace(0., float(segs), newlen ))
	ar_tiempo = np.linspace(0, len(datos)/nuevorate, len(datos))
	
	Vm = np.max(datos)-np.min(datos)
	Vc =  np.max(carrier)-np.min(carrier)
	M = Vm/(pm)
	datosAM = ((1+(datos/M))*carrier)
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

# Grafico AM convencional
def graficoAM(datos, rate,nuevorate, p, st = False, demod = False, pm = 1, color = 'g', titulo=''):
	pm = 10*pm
	w0 =  np.pi*nuevorate/4
	segs = len(datos)/rate
	newlen = nuevorate*len(datos)/rate

	datos = resample(datos, newlen)

	carrier = np.cos(w0*np.linspace(0., float(segs), newlen ))
	ar_tiempo = np.linspace(0, len(datos)/nuevorate, len(datos))
	
	Vm = np.max(datos)-np.min(datos)
	Vc =  np.max(carrier)-np.min(carrier)
	M = Vm/(pm)
	datosAM = datos*carrier
	p.set_title(titulo)
	if(demod):
		datosAM = fir_filter_lp(datosAM,nuevorate,4096,1000)
		p.set_title("Señal Demodulada")
	if(st):
		transformada = fft(datosAM)
		freq = fftfreq(transformada.size, 1/nuevorate)
		p.plot(freq, transformada, 'r')
		return
	p.plot(ar_tiempo, (datosAM), color)
	p.set_xlim(limitesx[0], limitesx[1])
	return (datosAM,carrier)

# Grafico FM para la señal dada

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
# Grafico AM
datosAM,carrier = graficoAM(info, rate,500000, plots[0], pm=1.0, color='c', titulo = 'Señal AM')
graficoTiempo(info, rate, plots[0]) 
# Grafico modulado FM
graficoFM(info, rate,2000000,50, plots[1], titulo = "Señal FM")
graficoTiempo(info, rate, plots[1]) 

# Grafico señal demodularizada AM
graficoAM(datosAM, 500000,500000, plots[2], st=False, demod=True, color='g')
# Comparando con señal original
graficoTiempo(info, rate, plots[2])
leg_demod = mpatches.Patch(color='g', label='Señal demodulada')
leg_origin = mpatches.Patch(color='r', label='Señal original')
plots[2].legend(handles=[leg_demod, leg_origin], prop={'size':7})

f.show()
f.savefig("figura1a.pdf")

# Parte 1.b

f, plots = plt.subplots(3)
f.subplots_adjust( hspace=1 )
# Modulacion a distintos porcentajes

graficoAMMod(info, rate,500000, plots[0], pm=0.5, color = 'r', titulo = 'Señal AM modulada al 50%')
graficoAMMod(info, rate,500000, plots[1], pm=1.0, color = 'g', titulo = 'Señal AM modulada al 100%')
graficoAMMod(info, rate,500000, plots[2], pm=2.0, color = 'b', titulo = 'Señal AM modulada al 200%')

f.show()
f.savefig("figura1b1.pdf")

f, plots = plt.subplots(3)
f.subplots_adjust( hspace=1 )
# Espectro de frecuencias para señales
graficoFrecuencia(info, rate, plots[0], titulo = "Frecuencia Señal Original")
graficoAM(info, rate,200000, plots[1], pm=1.0, st = True,color = 'r', titulo = 'Frecuencia Señal AM')
graficoFM(info, rate,2000000,50, plots[2], titulo = "Frecuencia Señal FM", st = True)


f.show()
f.savefig("figura1b2.pdf")
input("Presione enter para salir:\n")
