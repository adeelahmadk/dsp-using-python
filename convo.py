import numpy as np

x = [1.0, 2.0, 3.0, 4.0]
h = [1.0, 2.0, 3.0, 4.0]
len_x = len(x)
len_h = len(h)

# Linear convolution
y_linear = np.convolve(x, h)

print(f'x(n) = {x}')
print(f'h(n) = {h}')
print(f'Y_linear(n) = {y_linear}')

# Circular convolution wrong
X = np.fft.fft(x)
H = np.fft.fft(h)
y_circular_wrong = np.multiply(X, H)
y_circular_wrong = np.fft.ifft(y_circular_wrong)
print(f'Y_circular_wrong(n) = {y_circular_wrong.real}')

# Circular convolution with zero padding
N = len_x + len_h - 1
X = np.fft.fft(x, N) # if len(x) < N, zero pads the sequence
H = np.fft.fft(h, N)
y_circular_correct = np.multiply(X, H)
y_circular_correct = np.fft.ifft(y_circular_correct)
print(f'y_circular_correct(n) = {y_circular_correct.real}')

#freq = np.fft.fftfreq(t.shape[-1])
