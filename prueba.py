# -*- coding: utf-8 -*-
import numpy as np
from scipy.io.wavfile import read, write
import matplotlib.pyplot as plt
import matplotlib
import math
from scipy.fftpack import fft, fftfreq, ifft
from scipy.signal import *
from scipy import integrate


x0 = 0.001
largo = 0.003
limitesx = (x0, x0+largo)

rate,info = read('handel.wav')
seg = len(info)/rate
#info = info[:rate]
info = resample(info, len(info)*3)


x = np.linspace(0, seg, len(info))
for d in [50,75,100,150,200]:
	#sig = (1+(np.sin(2*np.pi*x/10))*d/100)*np.cos(2*np.pi*3*x)
	sig = (np.max(info)-np.min(info)+(info)*d/100)*np.cos(2*np.pi*30000*x)
	plt.plot(x, sig)
	plt.xlim(limitesx)
	plt.title("%d"%d)
	plt.show()