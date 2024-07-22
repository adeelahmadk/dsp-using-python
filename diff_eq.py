# Difference equation, FFT, frequency response
import numpy as np
import matplotlib.pyplot as plt
import math

def system_response_fft(num, den, N):
    """
    Computes frequecy & phase response of a system using FFT
    
    arg:    num coeffs of numerator polynomial
    arg:    den coeffs of denomenator polynomial
    arg:    N   resolution/points of FFT
    
    return:     H(k)    frequency response
                H(phi)  phase response
    """
    FFT_num = np.fft.fft(num, N)
    FFT_den = np.fft.fft(den, N)
    H = FFT_num / FFT_den
    H_frac = H.imag / H.real
    H_phi = 180 * np.arctan(H_frac) / np.pi
    return H, H_phi


def system_response_series(num, den, N_FFT):
    """
    Computes frequecy & phase response of a system
    using transfer function expansion.
    
    arg:    num coeffs of numerator polynomial
    arg:    den coeffs of denomenator polynomial
    arg:    N   resolution/points of FFT
    
    return:     H(w)    frequency response
                H(phi)  phase response
    """
    om = np.linspace(0, 2*np.pi, N_FFT) # omega
    n1, d1 = 0, 0
    len_poly = max(len(num), len(den))
    # z^jw terms
    zk = np.array([np.cos(k*om) - np.sin(k*om)*1j
                    for k in range(len_poly)])

    for n, z in zip(num, zk):  # sum numerator series
        n1 += n * z

    for d, z in zip(den, zk):  # sum denomenator series
        d1 += d * z

    H2 = n1 / d1  # frequency response
    ph_n = np.arctan(n1.imag / n1.real)
    ph_d = np.arctan(d1.imag / d1.real)
    H_phase = 180 * (ph_n - ph_d) / np.pi # phase response
    
    return H2, H_phase


# coefficients of the difference equation
num = [2.0, -1.8, 0.36]
den = [1.0, -0.325, 0.0187]

# FFT parameters
N_FFT = 512
Fs = 1000
f = np.linspace(0.0, Fs, N_FFT)

### H(k): using FFT
H1, H1_phi = system_response_fft(num, den, N_FFT)

### H(omega): using transfer function
H2, H2_phase = system_response_series(num, den, N_FFT)

### plot
# freq resp.
plt.figure(1)
plt.clf()
plt.subplot(1,2,1)
plt.plot(f, np.absolute(H1), 'b')
plt.grid()
plt.xlabel('f (Hz)')
plt.title('Response $|H(k)|$')

plt.subplot(1,2,2)
plt.plot(f, np.absolute(H2), 'b')
plt.grid()
plt.xlabel('f (Hz)')
plt.title('Response $|H(\omega)|$')

plt.savefig('fig/diffeq1.png')

# phase resp.
plt.figure(2)
plt.clf()
plt.subplot(1,2,1)
plt.plot(f, H1_phi, 'b')
plt.grid()
plt.xlabel('f (Hz)')
plt.title('Phase $|H(k)|$')

plt.subplot(1,2,2)
plt.plot(f, H2_phase, 'b')
plt.grid()
plt.xlabel('f (Hz)')
plt.title('Phase $|H(\omega)|$')

plt.savefig('fig/diffeq2.png')

plt.show()

