# -*- coding: utf-8 -*-
import numpy as np
from scipy.io.wavfile import read, write
import matplotlib.pyplot as plt
import matplotlib
import math
from scipy.fftpack import fft, fftfreq, ifft
from scipy.signal import *
from scipy import integrate
from binarizacion import *


def graficarConstelacion(datos, color, marc, msize = 5):
	plt.plot(*zip(*datos), marker=marc, color=color, ls='', markersize=msize)
def generarArreglo(arreglo, ind):
	return [ [r, i] for r,i in zip(np.real(arreglo[ind]), np.imag(arreglo[ind])) ]

#Leyendo el archivo
rate,info = read('handel.wav')
datosBinarizados = binarizar(info, 10**5)
originalQM = modularQM(datosBinarizados)
for dB in [-2,0,4,7,10]:
	ruidoQM = add_ruido(originalQM, dB)
	dm = demodularQM(ruidoQM)
	debin = debinarizar(dm)

	b=ruidoQM

	# Diferenciando valores originales
	indices = [[],[],[],[]]
	for index, e in enumerate(originalQM):
		if(e == 1+1j):
			indices[0].append(index)
		elif(e ==-1+1j):
			indices[1].append(index)
		elif(e == 1-1j):
			indices[2].append(index)
		else:
			indices[3].append(index)


	# Graficando constelacion con colores
	# A partir de los valores originales

	a00 = generarArreglo(b, indices[0])
	a01 = generarArreglo(b, indices[1])
	a10 = generarArreglo(b, indices[2])
	a11 = generarArreglo(b, indices[3])

	marcador = 'o'
	graficarConstelacion(a00, 'g', marcador)
	graficarConstelacion(a01, 'r', marcador)
	graficarConstelacion(a10, 'y', marcador)
	graficarConstelacion(a11, 'b', marcador)
	graficarConstelacion([[1,1],[1,-1],[-1,1],[-1,-1]], 'c', '*', 20)


	plt.title("QAM con ruido (%ddB)"%dB)
	plt.axhline(y=0, color='k')
	plt.axvline(x=0, color='k')
	plt.grid(True)
	plt.savefig("nube_%sdB.pdf"%dB)
	plt.ylabel("Q")
	plt.xlabel("I")
	plt.show()


f, plots = plt.subplots(2)
f.subplots_adjust( hspace=0.4 )
f.suptitle("Modulación Digital")

plots[0].set_title("Señal original")
plots[1].set_title("Señal demodulada con ruido (%ddB)"%dB)

plots[0].grid(True)
plots[1].grid(True)

# Graficando 10^5 bits con ruido
plots[1].plot(debin)
# Graficando 10^5 bits = 6250 enteros
plots[0].plot(info[:6250])


f.show()
f.savefig("figura2a.pdf")
input("Presione enter para seguir:\n")