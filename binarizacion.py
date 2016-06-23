import numpy as np

def binarizar(signal,themaczimo):
	binarysignal =[]
	for index,i in enumerate(signal):
		if((index+1)*16>themaczimo):
			break
		signo = (1,0)[i>0]
		aux = abs(i)
		#number = []
		for j in range(15):
			#number.append(aux&1)
			binarysignal.append(aux&1)
			aux = aux >> 1
		#number.append(signo)
		binarysignal.append(signo)
	return binarysignal

def debinarizar(binarysignal):
	signal=[]
	numero=0
	for i,b in enumerate(binarysignal):
		if((i+1)%16==0):
			numero=numero * (1,-1)[b]
			signal.append(numero)
			numero=0
		else:
			numero=numero|b<<(i%16)
	return signal

def modularQM(binarysignal,conruido=False):
	'''        |
		-1  1  |   1  1
		  01   |    00  
		-------+--------
		  11   |    10  
		-1 -1  |   1 -1 
		       |
	'''
	signal = []
	mem = 0
	for i,data in enumerate(binarysignal):
		if((i+1)%2==0):
			if(mem==0):
				if(data==0):
					signal.append(1+1j)
				else:
					signal.append(-1+1j)
			else:
				if(data==0):
					signal.append(1-1j)
				else:
					signal.append(-1-1j)
		else:
			mem = data

	return np.array(signal)

def add_ruido(qmSignal,db):
	d=1/(10**(db/10.0))**.5
	size=len(qmSignal)
	ruido=(np.random.normal(0,d,size)+np.random.normal(0,d,size)*1j)
	return qmSignal+ruido

def demodularQM(qmSignal):
	binarysignal=[]
	vector = np.array([1+1j,-1+1j,1-1j,-1-1j])
	for i,d in enumerate(qmSignal):
		n = np.argmax(abs(vector+d))
		binarysignal.append((n>>1)&1)
		binarysignal.append(n&1)
	return binarysignal
a=[  0,-202,-2459,-1021,202,1248,618,-820,-1021,-2459,-4123,-4728,-5939,-6241,-2459,-416,-1248,-2459,0,2459,4123,5939,4930,4123,2660,1853,0,-2055,-3114,-1248,-202,-618,-2459,-3114,-2459,-2459,-1021,-1853,-618,820,1853,1853,820,-618,820,3518,4123,2660,1021,202,-1021,202,-202,820,3921,4930,5334,5334,1652,0]
b=binarizar(a,1e15)
c=modularQM(b)
d=demodularQM(c)
print(a)
#print(c)
print(debinarizar(d))



