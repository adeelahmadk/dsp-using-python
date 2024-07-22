import matplotlib.pyplot as plt
import numpy as np
import math
from numpy import arange
from wfutils import read_uint16

# open binary file
FileName = 'data/ecg/ath_001.dat'

with open(FileName, 'rb') as file:
    byte_content = file.read()

# unpacking 16-bit little endian data
tmp1 = read_uint16(byte_content)
d = tmp1.astype(float)

"""
tmp4 = []
BigData = pow(2, 16)

for cnt in range(len(d)):
    tmp2 = d[cnt]
    if tmp2 >= 511:
        tmp3 = tmp2 - BigData
    else:
        tmp3 = tmp2
    
    tmp4.append(tmp3)
"""

Fs = 500 #200
Ts = 1/Fs
Cols = 12
Rows = int(len(d) / Cols)
d = (d - 1024) / 50000
ECG = np.reshape(d, (Rows, Cols))
dt = 4 # sec.
t = arange(0.0, (float(Fs * dt))*Ts, Ts)
TestLead = 2

plt.clf()
plt.figure(1)
#plt.subplot(2,1,1)
plt.plot(t, ECG[:(Fs * dt), TestLead], 'b')
plt.grid()
plt.xlabel('t (sec.)')
plt.ylabel('s(t)')
plt.title(f'ECG Signal: Test Lead {TestLead}')

plt.savefig('ecg_signal.png')

plt.show()

