"""
 IIR filter frequency & phase response
 
 - Using exp(jw) - 1 in the transfer function,
   1 at w = pi, 0 at w = 0
   gives a real zero at 1
 - Zero at z = 1
 - Pole at z = -alpha
 
 alpha = 0.9
 Fs = 1000 Hz
 fc = 483.37 Hz
"""
import numpy as np
import matplotlib.pyplot as plt

from lti import system_response_fft, find_hpf_cutoff, pz_plot


def main():
    ### IIR
    alpha = 0.9
    Factor = (1 - alpha) / 2
    num = [Factor, -Factor]
    den = [1.0, alpha]
    N_FFT = 512
    Fs = 1000

    resp_fig_filename = 'fig/iir_hpf1.png'
    pz_fig_filename = 'fig/iir_hpf1_pzplot.png'

    ### H(k)
    H1, H1_phi = system_response_fft(num, den, N_FFT)
    H1_abs = np.absolute(H1)
    H1_phi[0] = H1_phi[1]
    f = np.linspace(0.0, Fs, N_FFT)
    fc = find_hpf_cutoff(f, H1_abs)

    print(f'fc = {fc:.2f} Hz')

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
    
    plt.suptitle(f'HPF with $f_c = ${fc:.2f} Hz')
    plt.subplots_adjust(hspace=0.3)

    plt.savefig(resp_fig_filename)

    pz_plot(num, den, title='HPF Pole-Zero Plot')
    plt.savefig(pz_fig_filename)
    
    plt.show()


if __name__ == '__main__':
    main()

