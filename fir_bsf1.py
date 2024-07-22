"""
 FIR filter frequency & phase response
 
 Replace sine with cosine in the BPF function,
 1 at w = 0, pi, 0 at w = pi/2
 zeros become complex conjugate (-j, J)
 
 Fs = 1000 Hz
 fc1 = 123.29 Hz
 fc2 = 373.78 Hz
"""
import numpy as np
import matplotlib.pyplot as plt

from lti import system_response_fft, find_bsf_cutoff, pz_plot


def main():
    ### FIR
    num = [0.5, 0, 0.5]
    den = [1.0, 0, 0]
    N_FFT = 512
    Fs = 1000

    resp_fig_filename = 'fig/fir_bsf1.png'
    pz_fig_filename = 'fig/fir_bsf1_pzplot.png'

    ### H(k)
    H1, H1_phi = system_response_fft(num, den, N_FFT)
    H1_abs = np.absolute(H1)
    f = np.linspace(0.0, Fs, N_FFT)
    fc1, fc2 = find_bsf_cutoff(f, H1_abs)

    print(f'fc1 = {fc1:.2f} Hz, fc2 = {fc2:.2f} Hz')
    
    ### plot
    # freq resp.
    plt.figure(1)
    plt.clf()
    plt.subplot(2,1,1)
    plt.plot(f, H1_abs, 'b')
    plt.grid()
    plt.xlabel('f (Hz)')
    plt.ylabel('$|H(k)|$')
    #plt.title('Amplitude Response $|H(k)|$')

    # phase resp.
    plt.subplot(2,1,2)
    plt.plot(f, H1_phi, 'b')
    plt.grid()
    plt.xlabel('f (Hz)')
    plt.ylabel('$\Phi^{\circ}$')
    #plt.title('Phase Response $\Phi(H(k))$')
    
    plt.suptitle(f'BSF with $f_c = [${fc1:.2f} Hz, {fc2:.2f} Hz$]$')
    plt.subplots_adjust(hspace=0.5)

    plt.savefig(resp_fig_filename)
    
    pz_plot(num, den, title='BSF Pole-Zero Plot')
    plt.savefig(pz_fig_filename)

    plt.show()


if __name__ == '__main__':
    main()

