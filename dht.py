# Discrete Heartly Transform
import numpy as np
import matplotlib.pyplot as plt

def dht(x: np.array):
    X = np.fft.fft(x)
    X = X.real - X.imag
    return X

def idht(X: np.array):
    n = len(X)
    x = dht(X)
    x = 1/n * x
    return x


Fs = 200
Ts = 1 / Fs
Duration = 2
N = Duration * Fs
t = np.linspace(start=0.0, stop=Duration-Ts, num=N)
x = np.cos(2*np.pi*t)
N = len(x)

# DHT
X_DHT = np.zeros(N)
k = 0
while k < N:
    tmp1 = 0
    n = 0
    while n < N:
        term1 = 2 * np.pi * n * k / N
        tmp2 = x[n]*(np.cos(term1) + np.sin(term1))
        tmp1 += tmp2
        n += 1
    X_DHT[k] = tmp1
    k += 1

# IDCT
x2 = np.zeros(N)
n = 0
while n < N:
    tmp1 = 0
    k = 0
    while k < N:
        term1 = 2 * np.pi * n * k / N
        tmp2 = X_DHT[k]*(np.cos(term1) + np.sin(term1))
        tmp1 += tmp2
        k += 1
    x2[n] = tmp1 / N
    n += 1

X_DHT3 = dht(x)
x3 = idht(X_DHT3)


