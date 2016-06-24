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


dB = 10

#Leyendo el archivo
rate,info = read('handel.wav')
print(info[:60])
datosBinarizados = binarizar(info, 10**5)

originalQM = modularQM(datosBinarizados)
ruidoQM = add_ruido(originalQM, dB)
dm = demodularQM(ruidoQM)
debin = debinarizar(dm)

b=ruidoQM

# Diferenciando 
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



a00 = [ [r, i] for r,i in zip(np.real(b[indices[0]]), np.imag(b[indices[0]])) ] 
a01 = [ [r, i] for r,i in zip(np.real(b[indices[1]]), np.imag(b[indices[1]])) ] 
a10 = [ [r, i] for r,i in zip(np.real(b[indices[2]]), np.imag(b[indices[2]])) ] 
a11 = [ [r, i] for r,i in zip(np.real(b[indices[3]]), np.imag(b[indices[3]])) ] 



marcador = 'H'
plt.plot(*zip(*a00), marker=marcador, color='g', ls='')
plt.plot(*zip(*a01), marker=marcador, color='r', ls='')
plt.plot(*zip(*a10), marker=marcador, color='y', ls='')
plt.plot(*zip(*a11), marker=marcador, color='b', ls='')
plt.title("asdasd")
plt.axhline(y=0, color='k')
plt.axvline(x=0, color='k')
plt.grid(True)
plt.savefig("nube_%sdB.eps"%dB)
plt.ylabel("Q")
plt.xlabel("I")
plt.show()

f, plots = plt.subplots(2)
f.suptitle("Modulación Digital")
plots[0].grid(True)
plots[1].grid(True)
f.subplots_adjust( hspace=1 )

plots[0].plot(debin)
plots[1].plot(info[:6250])
plots[1].grid(True)

plots[1].axhline(y=0, color='k')
plots[1].axvline(x=0, color='k')

f.show()
f.savefig("figura2a.eps")
input("Presione enter para seguir:\n")