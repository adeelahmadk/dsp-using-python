# FIR filter frequency & phase response
# Fs = 1000 Hz
# fc = 248.53 Hz
import numpy as np
import matplotlib.pyplot as plt

from lti import system_response_fft, find_lpf_cutoff, pz_plot


def main():
    ### FIR
    num = [0.25, 0.5, 0.25]
    den = [1.0, 0]
    N_FFT = 512
    Fs = 1000

    resp_fig_filename = 'fig/fir_lpf2.png'
    pz_fig_filename = 'fig/fir_lpf2_pzplot.png'

    ### H(k)
    H1, H1_phi = system_response_fft(num, den, N_FFT)
    H1_abs = np.absolute(H1)
    f = np.linspace(0.0, Fs, N_FFT)
    fc = find_lpf_cutoff(f, H1_abs)
    zeros = np.roots(num)

    print(f'Zeros at {zeros}')
    print(f'fc = {fc:.2f} Hz')

    ### plot
    # freq resp.
    plt.figure(1)
    plt.clf()
    plt.subplot(2,1,1)
    plt.plot(f, H1_abs, 'b')
    plt.grid()
    plt.xlabel('f (Hz)')
    #plt.title('Amplitude Response $|H(k)|$')

    # phase resp.
    plt.subplot(2,1,2)
    plt.plot(f, H1_phi, 'b')
    plt.grid()
    plt.xlabel('f (Hz)')
    #plt.title('Phase Response $\Phi(H(k))$')

    plt.suptitle(r'$2^{nd}$ ' f'order LPF with $f_c = ${fc:.2f} Hz')
    plt.subplots_adjust(hspace=0.3)
    
    plt.savefig(resp_fig_filename)

    pz_plot(num, den, title='$2^{nd}$ order LPF Pole-Zero Plot')
    plt.savefig(pz_fig_filename)

    plt.show()


if __name__ == '__main__':
    main()

