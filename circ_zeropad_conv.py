import numpy as np

x = np.linspace(1., 8., 8)
h = [-10.0, -11.0, -12.0]
len_x = len(x)
len_h = len(h)

# Linear convolution
y_linear = np.convolve(x, h)

print(f'x(n) = {x}')
print(f'h(n) = {h}')
print(f'Y_linear(n) = {y_linear}')

# Circular convolution with zero padding
N = len_x + len_h - 1
X = np.fft.fft(x, N) # if len(x) < N, zero pads the sequence
H = np.fft.fft(h, N)
y_circular = np.multiply(X, H)
y_circular = np.fft.ifft(y_circular)
y_imag = y_circular.imag
y_real = y_circular.real
fnd = abs(y_imag) < 0.0000001
y_imag[fnd] = 0
y_circular.imag = y_imag
print(f'y_circular(n) = {y_circular.real}')

#freq = np.fft.fftfreq(t.shape[-1])
