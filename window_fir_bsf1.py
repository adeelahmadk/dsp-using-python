"""
  FIR BSF filter using Hanning window
  Fs = 8 kHz,
  fs1 = 2 kHz,
  fs2 = 3 kHz,
  df = 800 Hz
  As > 40 dB
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

from lti import find_bsf_cutoff, find_bsf_stopband


def main():
    ### params
    N = 31          # degree
    As = 40         # db
    df = 800        # width of transition region
    fs1 = 2000      # stopband freq 1
    fs2 = 3000      # stopband freq 2
    Fs = 8000       # sampling freq
    N_FFT = 1024
    fig_filename = 'fig/windowed_fir_bsf1.png'
    
    ### FIR coeffs
    fc1 = fs1 - df
    fc2 = fs2 + df
    num = signal.firwin(N, [fs1, fs2], width=df,
                        window='hanning',
                        pass_zero=True,  # DC gain = 1
                        fs=Fs)
    den = np.zeros(len(num))
    den[0] = 1.0
    
    ### frequency response
    f, H = signal.freqz(num, den, worN=N_FFT, fs=Fs)
    H_abs = np.absolute(H)
    fc_computed = find_bsf_cutoff(f, H_abs)
    fs_computed = find_bsf_stopband(f, H_abs, As)
    df_computed = [0, 0]
    df_computed[0] = fs_computed[0] - fc_computed[0]
    df_computed[1] = fc_computed[1] - fs_computed[1]
    print(f'fc_computed = {fc_computed[0]:.2f} Hz, {fc_computed[1]:.2f} Hz')
    print(f'fs_computed = {fs_computed[0]:.2f} Hz, {fs_computed[1]:.2f} Hz')
    print(f'df_computed = {df_computed[0]} Hz, {df_computed[1]:.2f} Hz')
    
    ### plot
    y = np.linspace(0, 1, 100)
    x_fc1_computed = fc_computed[0] * np.ones(len(y))
    x_fc2_computed = fc_computed[1] * np.ones(len(y))
    x_fs1_computed = fs_computed[0] * np.ones(len(y))
    x_fs2_computed = fs_computed[1] * np.ones(len(y))
    
    fig, ax = plt.subplots()
    ax.plot(f, H_abs, 'b')
    ax.plot(x_fc1_computed, y, 'g--', x_fs1_computed, y, 'r--')
    ax.plot(x_fc2_computed, y, 'g--', x_fs2_computed, y, 'r--')
    ax.set(xlabel='f (Hz)', title='|H(k)|')
    
    ## annotations
    # fc ->
    ax.annotate("", xy=(fc_computed[0], H_abs[np.nonzero(f==fc_computed[0])]),
            xytext=(fc_computed[0]+250, H_abs[np.nonzero(f==fc_computed[0])]),
            arrowprops=dict(arrowstyle="->", connectionstyle="arc3"))
    ax.text(fc_computed[0]+250, H_abs[np.nonzero(f==fc_computed[0])],
        '$f_c$', color="green", fontsize=12,
        horizontalalignment="left", verticalalignment="center")
    
    # fs <->
                    # from fs1 to fs2
    ax.annotate("", xy=(fs_computed[0], 0.05),
            xytext=(fs_computed[1], 0.05),
            arrowprops=dict(arrowstyle="<->", connectionstyle="arc3"))
    ax.text(fs_computed[0]+(fs_computed[1]-fs_computed[0])/2, 0.1,
        '$f_s$', color="red", fontsize=12,
        horizontalalignment="center", verticalalignment="center")
    
    # df <->
                    # from fc1 to fs1
    ax.annotate("", xy=(fc_computed[0], 0.01),
            xytext=(fs_computed[0], 0.01),
            arrowprops=dict(arrowstyle="<->", connectionstyle="arc3"))
    ax.text(fc_computed[0]+df_computed[0]/2, -0.03,
            '$df$', color="blue", fontsize=14,
            horizontalalignment="center", verticalalignment="center")
    
    ax.legend(("freq. response", "cut-off freq.", "stopband edge"),
          shadow=True, loc=(0.02, 0.73), handlelength=1.5, fontsize=12)

    # results
    txt = (r'$f_{c1}=$'
            f'{fc_computed[0]:.2f} Hz')
    ax.text(50, 0.62, txt, color="green", fontsize=12,
        horizontalalignment="left", verticalalignment="center")
    txt = (r'$f_{c2}=$'
            f'{fc_computed[1]:.2f} Hz')
    ax.text(50, 0.55, txt, color="green", fontsize=12,
        horizontalalignment="left", verticalalignment="center")
    txt = (r'$f_{s1}=$'
            f'{fs_computed[0]:.2f} Hz')
    ax.text(50, 0.48, txt, color="red", fontsize=12,
        horizontalalignment="left", verticalalignment="center")
    txt = (r'$f_{s2}=$'
            f'{fs_computed[1]:.2f} Hz')
    ax.text(50, 0.41, txt, color="red", fontsize=12,
        horizontalalignment="left", verticalalignment="center")

    ax.grid()
    
    plt.savefig(fig_filename)
    
    plt.show()    


if __name__ == '__main__':
    main()

