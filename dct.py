# Discrete Cosine Transform
import numpy as np
import matplotlib.pyplot as plt


def dct(x: np.array) -> np.array:
    """
    Computes DCT of signal samples.
    """
    N = x.shape[0]
    X_DCT = np.zeros(N)
    ck0 = 1 / np.sqrt(2)
    ck1 = 1

    k = 0
    while k < N:
        if k == 0:
            ck = ck0
        else:
            ck = ck1
        
        tmp1 = 0
        n = 0
        while n < N:
            tmp2 = x[n]*ck*np.cos(((2*n+1)*k*np.pi) / (2*N))
            tmp1 += tmp2
            n += 1
        X_DCT[k] = tmp1
        k += 1

    return X_DCT


def idct(X: np.array) -> np.array:
    """
    Computes IDCT of a signal's spectrum samples.
    """
    N = X.shape[0]
    x = np.zeros(N)
    ck0 = 1 / np.sqrt(2)
    ck1 = 1
    
    n = 0
    while n < N:
        tmp1 = 0
        k = 0
        while k < N:
            if k == 0:
                ck = ck0
            else:
                ck = ck1

            tmp2 = X[k]*ck*np.cos(((2*n+1)*k*np.pi) / (2*N))
            tmp1 += tmp2
            k += 1
        x[n] = 2/N * tmp1
        n += 1

    return x


def main():
    # prepare signal
    Fs = 200
    Ts = 1 / Fs
    Duration = 2
    N = Duration * Fs
    t = np.linspace(start=0.0, stop=Duration-Ts, num=N)
    x = np.cos(2*np.pi*t)

    # perform transforms
    X_DCT = dct(x)
    x2 = idct(X_DCT)
    freq = np.fft.fftfreq(t.shape[-1])

    # plots
    plt.rcParams['text.usetex'] = True

    plt.clf()
    plt.figure(1)
    plt.subplot(1,2,1)
    plt.plot(x, 'b')
    plt.grid()
    plt.title('Original Signal')

    plt.subplot(1,2,2)
    plt.plot(x2, 'b')
    plt.grid()
    plt.title('Reconstructed Signal from IDCT')

    plt.figure(2)
    plt.plot(X_DCT.real / N, 'b')
    plt.grid()
    plt.xlabel('$Cycles / T_s$')
    plt.ylabel(r'$real(H(\omega))$')
    plt.title('Signal Spectrum')

    plt.show()


if __name__ == '__main__':
    main()

