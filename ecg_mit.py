import matplotlib.pyplot as plt
import numpy as np
import math
from numpy import arange
import wfutils

def read_uint12(data_chunk):
    """
    unpacks 12-bit little endian data into numpy array
    """
    data = np.frombuffer(data_chunk, dtype=np.uint8)
    fst_uint8, mid_uint8, lst_uint8 = np.reshape(data, (data.shape[0] // 3, 3)).astype(np.uint16).T
    fst_uint12 = ((mid_uint8 & 0x0F) << 8) | fst_uint8
    snd_uint12 = (lst_uint8 << 4) | ((mid_uint8 & 0xF0) >> 4)
    return np.reshape(np.concatenate((fst_uint12[:, None], snd_uint12[:, None]), axis=1), 2 * fst_uint12.shape[0])


Fs = 360
Ts = 1/Fs
ADC_offset = 1024   # units
ADC_gain = 200      # units / mV

# open binary file
FileName = 'data/ecg/100.dat'

with open(FileName, 'rb') as file:
    byte_content = file.read()

unpaked_data = wfutils.read_uint12(byte_content)

Cols = 2
Rows = int(unpaked_data.shape[0] // Cols)
dt = 4 # sec.

ECG = np.reshape(unpaked_data, (Rows, Cols)).astype(float)
ECG = (ECG - ADC_offset) / ADC_gain
t = arange(0.0, (float(Fs * dt))*Ts, Ts) # 10 sec.

plt.rcParams['text.usetex'] = True
plt.rcParams['font.family'] = 'sans-serif'

plt.clf()
plt.figure(1, figsize=(8,6))

plt.subplot(2,1,1)
TestLead = 0
plt.plot(t, ECG[:(Fs * dt), TestLead], 'b')
plt.grid()
#plt.xlabel('t (sec.)')
plt.ylabel(r'$\textbf{MLII}, \mathbf{s_1(t)}$')
#plt.title('Lead 1: MLII')

plt.subplot(2,1,2)
TestLead = 1
plt.plot(t, ECG[:(Fs * dt), TestLead], 'b')
plt.grid()
plt.xlabel('t (sec.)')
plt.ylabel(r'$\textbf{V1}, s_2(t)$')
#plt.title('Lead 2: V1')

plt.suptitle('MIT-BIH: ECG Signal 100')
plt.subplots_adjust(hspace=0.4)
plt.savefig('fig/ecg_mit100.png', dpi=300)

plt.show()

