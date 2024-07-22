"""
 FIR filter frequency & phase response
 
 Using j*sin(w) in the transfer function,
 1 at w = pi/2, 0 at w = 0, pi
 zeros become real repeated (-1, 1)
 
 Fs = 1000 Hz
 fc1 = 121.33 Hz
 fc2 = 375.73 Hz
"""
import numpy as np
import matplotlib.pyplot as plt

from lti import system_response_fft, find_bpf_cutoff, pz_plot


def main():
    ### FIR
    num = [0.5, 0, -0.5]
    den = [1.0, 0, 0]
    N_FFT = 512
    Fs = 1000

    resp_fig_filename = 'fig/fir_bpf1.png'
    pz_fig_filename = 'fig/fir_bpf1_pzplot.png'

    ### H(k)
    H1, H1_phi = system_response_fft(num, den, N_FFT)
    H1_abs = np.absolute(H1)
    f = np.linspace(0.0, Fs, N_FFT)
    fc1, fc2 = find_bpf_cutoff(f, H1_abs)

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
    
    plt.suptitle(f'BPF with $f_c = [${fc1:.2f} Hz, {fc2:.2f} Hz$]$')
    plt.subplots_adjust(hspace=0.3)

    plt.savefig(resp_fig_filename)

    pz_plot(num, den, title='BPF Pole-Zero Plot')
    plt.savefig(pz_fig_filename)

    plt.show()


if __name__ == '__main__':
    main()

