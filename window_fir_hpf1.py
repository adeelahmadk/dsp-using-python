"""
  FIR HPF filter using Hanning window
  Fs = 8 kHz,
  fp = 2 kHz,
  df = 800 Hz
  As > 40 dB
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

from lti import find_hpf_cutoff, find_hpf_stopband


def db20(array):
    with np.errstate(divide='ignore'):
        return 20 * np.log10(array)


def main():
    ### params
    N = 31          # degree
    As = 40         # db
    df = 800        # width of transition region
    fc = 2000       # cutoff freq
    Fs = 8000       # sampling freq
    N_FFT = 1024
    fig_filename = 'fig/windowed_fir_hpf1.png'
    
    ### FIR coeffs
    fs = fc - df
    num = signal.firwin(N, fc, width=df,
                        window='hanning',
                        pass_zero=False,  # DC gain = 0
                        fs=Fs)
    den = np.zeros(len(num))
    den[0] = 1.0
    
    ### frequency response
    f, H = signal.freqz(num, den, worN=N_FFT, fs=Fs)
    H_abs = np.absolute(H)
    fc_computed = find_hpf_cutoff(f, H_abs)
    fs_computed = find_hpf_stopband(f, H_abs, As)
    df_computed = fc_computed - fs_computed
    print(f'fc_computed = {fc_computed} Hz')
    print(f'fs_computed = {fs_computed} Hz')
    print(f'df_computed = {df_computed} Hz')
    
    ### plot
    y = np.linspace(0, 1, 100)
    x_fc_computed = fc_computed * np.ones(len(y))
    x_fs_computed = fs_computed * np.ones(len(y))
    
    fig, ax = plt.subplots()
    ax.plot(f, H_abs, 'b')
    ax.plot(x_fc_computed, y, 'g--', x_fs_computed, y, 'r--')
    ax.set(xlabel='f (Hz)', title='|H(k)|')
    
    ## annotations
    # fc ->
    ax.annotate("", xy=(fc_computed, H_abs[np.nonzero(f==fc_computed)]),
            xytext=(fc_computed+250, H_abs[np.nonzero(f==fc_computed)]),
            arrowprops=dict(arrowstyle="->", connectionstyle="arc3"))
    ax.text(fc_computed+250, H_abs[np.nonzero(f==fc_computed)],
        '$f_c$', color="green", fontsize=14,
        horizontalalignment="left", verticalalignment="center")
    
    # fs ->
    ax.annotate("", xy=(fs_computed, H_abs[np.nonzero(f==fs_computed)]),
            xytext=(fs_computed-250, H_abs[np.nonzero(f==fs_computed)]),
            arrowprops=dict(arrowstyle="->", connectionstyle="arc3"))
    ax.text(fs_computed-300, H_abs[np.nonzero(f==fs_computed)],
        '$f_s$', color="red", fontsize=14,
        horizontalalignment="right", verticalalignment="baseline")
    
    # df <->
    ax.annotate("", xy=(fc_computed, 0.01), xytext=(fs_computed, 0.01),
            arrowprops=dict(arrowstyle="<->", connectionstyle="arc3"))
    ax.text(fs_computed+df_computed/2, -0.03, '$df$', color="blue", fontsize=14,
        horizontalalignment="center", verticalalignment="center")
    
    ax.legend(("freq. response", "cut-off freq.", "stopband edge"),
          shadow=True, loc=(0.02, 0.73), handlelength=1.5, fontsize=12)
    
    # results
    txt = (r'$f_{s}=$'
            f'{fs_computed:.2f} Hz')
    ax.text(50, 0.62, txt, color="red", fontsize=12,
        horizontalalignment="left", verticalalignment="center")
    txt = (r'$f_{c}=$'
            f'{fc_computed:.2f} Hz')
    ax.text(50, 0.55, txt, color="green", fontsize=12,
        horizontalalignment="left", verticalalignment="center")

    ax.grid()
    
    plt.savefig(fig_filename)
    
    plt.show()    


if __name__ == '__main__':
    main()

