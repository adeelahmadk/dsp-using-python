"""
 FIR filter frequency & phase response
 
 - Using j*sin(w) in the transfer function,
   1 at w = pi/2, 0 at w = 0, pi
   zeros become real repeated (-1, 1)
  - Zeros: z = {β - sqrt(β^2 - 1), z = β + sqrt(β^2 - 1)}
  - Poles: z = 1/2 (-sqrt((-α β - β)^2 - 4 α^2) + α β + β)
 
 - Fs = 1000 Hz
 - Zeros at z = {z = 0.6 - 0.8j, z = 0.6 + 0.8j}
 - Poles at z = {0.57 - 0.69649j, 0.57 + 0.69649j}
 fc1 = 133.07 Hz
 fc2 = 180.04 Hz
"""
import numpy as np
import matplotlib.pyplot as plt

from lti import system_response_fft, find_bsf_cutoff, pz_plot


def main():
    ### IIR
    alpha = 0.9
    beta = 0.6
    Factor = (1 + alpha) / 2
    num = [Factor, -2*beta*Factor, Factor]
    den = [1.0, -beta * (1 + alpha), np.power(alpha, 2)]
    N_FFT = 512
    Fs = 1000

    resp_fig_filename = 'fig/iir_bsf1.png'
    pz_fig_filename = 'fig/iir_bsf1_pzplot.png'

    ### H(k)
    H1, H1_phi = system_response_fft(num, den, N_FFT)
    H1_abs = np.absolute(H1)
    #H1_phi[0] = H1_phi[1]
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
    
    plt.suptitle(f'BPF with $f_c = (${fc1:.2f} Hz, {fc2:.2f} Hz$)$')
    plt.subplots_adjust(hspace=0.3)

    plt.savefig(resp_fig_filename)

    pz_plot(num, den, title='BPF Pole-Zero Plot')
    plt.savefig(pz_fig_filename)

    plt.show()


if __name__ == '__main__':
    main()

