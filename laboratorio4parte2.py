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


#Leyendo el archivo
rate,info = read('handel.wav')
datosBinarizados = binarizar(info, 10**5)

originalQM = modularQM(datosBinarizados)
ruidoQM = modularQM(add_ruido(datosBinarizados, -2))


f, plots = plt.subplots(2)
f.suptitle("Modulación")
plots[0].grid(True)
plots[1].grid(True)
f.subplots_adjust( hspace=1 )

# Graficando
print(ruidoQM)
a=ruidoQM#[ [] for p in ruidoQM]
plots[0].plot(*zip(*a), marker='o', color='r', ls='')


f.show()
f.savefig("figura2a.eps")
input("Presione enter para seguir:\n")