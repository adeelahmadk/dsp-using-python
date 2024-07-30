# Functions for LTI systems
import numpy as np

def system_response_fft(num: np.array, den: np.array, N: int) -> tuple[np.array, : np.array]:
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
    # only divide by nonzeros else 0
    H_frac = np.zeros(H.shape[0])
    np.divide(H.imag, H.real, out=H_frac, where=H.real!=0)
    H_phi = 180 * np.arctan(H_frac) / np.pi
    return H, H_phi


def system_response_series(num: np.array, den: np.array, N: int) -> tuple[np.array, : np.array]:
    """
    Computes frequecy & phase response of a system
    using transfer function expansion.
    
    arg:    num coeffs of numerator polynomial
    arg:    den coeffs of denomenator polynomial
    arg:    N   resolution/points of FFT
    
    return:     H(w)    frequency response
                H(phi)  phase response
    """
    om = np.linspace(0, 2*np.pi, N) # omega
    n1, d1 = 0, 0
    len_poly = max(len(num), len(den))
    # z^jw terms
    zk = np.array([np.cos(k*om) - np.sin(k*om)*1j
                    for k in range(len_poly)])

    for n, z in zip(num, zk):  # sum numerator series
        n1 += n * z

    for d, z in zip(den, zk):  # sum denomenator series
        d1 += d * z

    H = n1 / d1  # frequency response
    ph_n = np.arctan(n1.imag / n1.real)
    ph_d = np.arctan(d1.imag / d1.real)
    H_phi = 180 * (ph_n - ph_d) / np.pi # phase response
    
    return H, H_phi


def find_lpf_cutoff(f: np.array, H1_abs: np.array) -> np.float64:
    """
    Returns cut-off frequency of an LPF
    """
    MaxAmp = np.max(H1_abs)
    TargetAmp = 1 / np.sqrt(2) * MaxAmp
    cnt = 0
    while H1_abs[cnt] > TargetAmp:
        cnt += 1

    fc = f[cnt - 1]
    return fc


def find_lpf_stopband(f: np.array, H1_abs: np.array, As: float) -> np.float64:
    """
    Returns stopband edge frequency of an LPF
    """
    delta_s = 10**(-As/20)
    MaxAmp = np.max(H1_abs)
    TargetAmp = delta_s
    fs = 0
    cnt = 0
    while H1_abs[cnt] > TargetAmp:
        if cnt >= len(H1_abs) - 1:
            return fs
        cnt += 1
    
    fs = f[cnt - 1]
    return fs
    

def find_hpf_cutoff(f: np.array, H1_abs: np.array) -> np.float64:
    """
    Returns cut-off frequency of an HPF
    """
    MaxAmp = np.max(H1_abs)
    TargetAmp = 1 / np.sqrt(2) * MaxAmp
    cnt = H1_abs.argmax()
    fc = 0
    #cnt = 0
    while H1_abs[cnt] > TargetAmp:
        if cnt <= 0:
            return fc
        cnt -= 1

    fc = f[cnt - 1]
    return fc


def find_hpf_stopband(f: np.array, H1_abs: np.array, As: float) -> np.float64:
    """
    Returns stopband edge frequency of an LPF
    """
    delta_s = 10**(-As/20)
    MaxAmp = np.max(H1_abs)
    TargetAmp = delta_s
    fs = 0
    cnt = H1_abs.argmax()
    while H1_abs[cnt] > TargetAmp:
        if cnt <= 0:
            return fs
        cnt -= 1
    
    fs = f[cnt - 1]
    return fs


def find_bpf_cutoff(f: np.array, H1_abs: np.array) -> tuple[np.float64, np.float64]:
    """
    Returns cut-off frequency of a BPF
    """
    MaxAmp = np.max(H1_abs)
    TargetAmp = 1 / np.sqrt(2) * MaxAmp
    MaxIdx = H1_abs.argmax()
    fc1, fc2 = 0, 0
    
    cnt = MaxIdx
    while H1_abs[cnt] > TargetAmp:
        if cnt <= 0:
            return fc1, fc2
        cnt -= 1

    fc1 = f[cnt - 1]

    cnt = MaxIdx
    while H1_abs[cnt] > TargetAmp:
        if cnt >= len(H1_abs) - 1:
            return fc1, fc2
        cnt += 1

    fc2 = f[cnt - 1]

    return fc1, fc2


def find_bpf_stopband(f: np.array, H1_abs: np.array, As: float) -> np.float64:
    """
    Returns stopband edge frequency of an BPF
    """
    delta_s = 10**(-As/20)
    MaxAmp = np.max(H1_abs)
    TargetAmp = delta_s
    fs1, fs2 = 0, 0
    MaxIdx = H1_abs.argmax()
    cnt = MaxIdx
    while H1_abs[cnt] > TargetAmp:
        if cnt <= 0:
            return fs1, fs2
        cnt -= 1
    
    fs1 = f[cnt - 1]

    cnt = MaxIdx
    while H1_abs[cnt] > TargetAmp:
        if cnt >= len(H1_abs) - 1:
            return fs1, fs2
        cnt += 1
    
    fs2 = f[cnt - 1]

    return fs1, fs2


def find_bsf_cutoff(f: np.array, H1_abs: np.array) -> tuple[np.float64, np.float64]:
    """
    Returns cut-off frequency of a BSF
    """
    MaxAmp = np.max(H1_abs)
    TargetAmp = 1 / np.sqrt(2) * MaxAmp
    fc1, fc2 = 0, 0
        
    cnt = 0
    while H1_abs[cnt] > TargetAmp:
        if cnt >= len(H1_abs) - 1:
            return fc1, fc2
        cnt += 1

    fc1 = f[cnt - 1]

    cnt = len(H1_abs) - 1
    while H1_abs[cnt] > TargetAmp:
        if cnt <= 0:
            return fc1, fc2
        cnt -= 1

    fc2 = f[cnt - 1]

    return fc1, fc2


def find_bsf_stopband(f: np.array, H1_abs: np.array, As: float) -> np.float64:
    """
    Returns stopband edge frequency of an BSF
    """
    delta_s = 10**(-As/20)
    MaxAmp = np.max(H1_abs)
    TargetAmp = delta_s
    fs1, fs2 = 0, 0
    
    cnt = 0
    while H1_abs[cnt] > TargetAmp:
        if cnt >= len(H1_abs) - 1:
            return fs1, fs2
        cnt += 1
    
    fs1 = f[cnt - 1]

    cnt = len(H1_abs) - 1
    while H1_abs[cnt] > TargetAmp:
        if cnt <= 0:
            return fs1, fs2
        cnt -= 1
    
    fs2 = f[cnt - 1]

    return fs1, fs2


def pz_plot(num: np.array, den: np.array, title: str='Pole-Zero Plot', show: bool=False, save_file: str=None) -> None:
    """
    Plots poles & zeros for a system's transfer function.
    """
    ### PZ
    zeros = np.roots(num).astype('complex')
    poles = np.roots(den).astype('complex')
    
    import matplotlib.pyplot as plt
    
    figure, axes = plt.subplots()
    theta = np.linspace( 0 , 2 * np.pi , 150 )
    r = 1.0
    a = r*np.cos(theta)
    b = r*np.sin(theta)
    axes.plot(a, b, 'r')
    axes.set_aspect(1)
    axes.plot(zeros.real, zeros.imag, 'o', 
        markerfacecolor='white', markeredgecolor='blue')
    axes.plot(poles.real, poles.imag, 'bx')
    plt.xlabel('Re(z)')
    plt.ylabel('Im(z)')
    plt.title(title)
    plt.grid()

    if save_file:
        plt.savefig(save_file)

    if show:
        plt.show()


