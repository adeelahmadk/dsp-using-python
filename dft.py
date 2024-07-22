import numpy as np

x = [1.0, 2.0, 3.0, 4.0]
X = np.fft.fft(x)
x_rec = np.fft.ifft(X)
print(f'x[n] = {x}')
print(f'X[k] = {X}')
print(f'recovered x[n] = {x_rec}')

