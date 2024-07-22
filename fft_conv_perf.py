# performance analysis of linear & zero-padded circular convolution
import numpy as np
import time

x = np.random.normal(0, 1, pow(10,5))
h = np.random.normal(0, 1, pow(10,4))
len_x = len(x)
len_h = len(h)

# Linear convolution
t1 = time.perf_counter()
y_linear = np.convolve(x, h)
elapsed1 = time.perf_counter() - t1
print(f'Time elapsed for linear conv = {elapsed1:.3f} sec.')

# Circular convolution with zero padding
N = len_x + len_h - 1
N2 = 1
while N2 < N:
    N2 *= 2
# N2 = np.power(2, np.ceil(np.log2(N))).astype(int)

t1 = time.perf_counter()
X = np.fft.fft(x, N) # if len(x) < N, zero pads the sequence
H = np.fft.fft(h, N)
y_circular = np.multiply(X, H)
y_circular = np.fft.ifft(y_circular)
y_imag = y_circular.imag
y_real = y_circular.real
fnd = abs(y_imag) < 0.0000001
y_imag[fnd] = 0
y_circular.imag = y_imag
elapsed2 = time.perf_counter() - t1

print(f'Time elapsed for circular conv = {elapsed2:.3f} sec.')
print(f'Ratio of Time elapsed = {(elapsed1 / elapsed2):.2f} times')

