# Programming Pattern Specifications

## Formats and Computations

### Reading & Unpacking Bit-Packed Data

While reading a bit-packed data (ADC data e.g. WFDB, audio, video etc.), we need to unpack it into standard data types before performing any kind of processing. We discuss some methods, in increasing order of efficiency, to unpack packed 12-bit little-endian data from ECG machine. The data used in these examples is WFDB format files taken from PysioNet.

#### Using Python `struct`

```python
for oo in range(0,len(byte_string)-2,3):
    (word,) = struct.unpack('<L', byte_string[oo:oo+3] + b'\x00')
    ii[ic+1], ii[ic] = (word >> 12) & 0xfff, word & 0xfff
    ic += 2
```

#### Using `numpy`

A more efficient method is to use numpy arrays. In this case upacking of little endian data looks like:

```python
def read_uint12(data_chunk):
    data = np.frombuffer(data_chunk, dtype=np.uint8)
    fst_uint8, mid_uint8, lst_uint8 = np.reshape(
      																	data,
      																	(data.shape[0] // 3, 3)
    																	).astype(np.uint16).T
    fst_uint12 = ((mid_uint8 & 0x0F) << 8) | fst_uint8
    snd_uint12 = (lst_uint8 << 4) | ((mid_uint8 & 0xF0) >> 4)
    return np.reshape(
              np.concatenate(
                (fst_uint12[:, None], snd_uint12[:, None]),
                axis=1
              ),
              2 * fst_uint12.shape[0]
    			)
```

In case of 12-bit packed binary image data, the packing is such that the "middle" byte contains the least significant nibbles. Bytes 1 and 3 of the triplet are the most significant 8 bits of the twelve bits. Therefore, the solution to this problem looks like:

```python
def read_uint12(data_chunk):
    data = np.frombuffer(data_chunk, dtype=np.uint8)
    fst_uint8, mid_uint8, lst_uint8 = np.reshape(
      																	data,
      																	(data.shape[0] // 3, 3)
    																	).astype(np.uint16).T
    fst_uint12 = (fst_uint8 << 4) | (mid_uint8 >> 4)
    snd_uint12 = (lst_uint8 << 4) | (np.bitwise_and(15, mid_uint8))
    return np.reshape(
      				np.concatenate(
                (fst_uint12[:, None], snd_uint12[:, None]),
                axis=1
              ),
      				2 * fst_uint12.shape[0]
    			)
```



### Branch vs. Compute

We can take one of two approaches while computing the nearest power of 2 greater than an integer.

```python
N = len_x + len_h - 1

# branching
N2 = 1
while N2 < N:
    N2 *= 2

# computing with math:
N2 = np.power(2, np.ceil(np.log2(N))).astype(int)
```



### Operations

#### Avoid Division by Indeterminate Forms

Replacing results of indeterminate forms after the operation still raises a warning.

```python
H_frac = H.imag / H.real
fnd = np.isnan(H_frac)
H_frac[fnd] = 0
```

This can be avoided by using `np.divide` with a pre-initialized array for storing output:

```python
H_frac = np.zeros(H.shape[0])
# only divide by nonzeros else 0
np.divide(H.imag, H.real, out=H_frac, where=H.real!=0)
```



### Difference Equations and Frequency Response

The iterative method of amplitude/phase response calculation

```python
H_phi = np.zeros(N_FFT)
cnt = 0
for cnt in range(0, N_FFT):
    H_phi[cnt] =
	    180 * math.atan(H_imag[cnt] / H_real[cnt]) / np.pi

```

is transformed to more pythonic idioms using operators overloaded for `numpy` data types:

```python
H_phi = 180 * np.arctan(H.imag / H.real) / np.pi
```

A solution specific to a polynomial length

```python
om = np.linspace(0, 2*np.pi, N_FFT)
a1 = np.cos(om) - np.sin(om)*1j
a2 = np.cos(2*om) - np.sin(2*om)*1j
n1 = 2.0 - 1.8*a1 + 0.36*a2
d1 = 1.0 - 0.325*a1 + 0.0187*a2
H2_abs = np.absolute(n1 / d1)
ph_n = np.arctan(n1.imag / n1.real)
ph_d = np.arctan(d1.imag / d1.real)
H2_phase = 180 * (ph_n - ph_d) / np.pi
```

is generalized in pythonic way:

```python
def system_response_series(num, den, N_FFT):
    """
    Computes frequecy & phase response of a system
    using transfer function expansion.
    
    arg:    num coeffs of numerator polynomial
    arg:    den coeffs of denomenator polynomial
    arg:    N   resolution/points of FFT
    
    return:     H(w)    frequency response
                H(phi)  phase response
    """
    om = np.linspace(0, 2*np.pi, N_FFT)
    n1, d1 = 0, 0
    len_poly = max(len(num), len(den))
    # e^jw terms
    zk = np.array([np.cos(k*om) - np.sin(k*om)*1j
                    for k in range(len_poly)])

    for n, z in zip(num, zk):  # sum numerator series
        n1 += n * z

    for d, z in zip(den, zk):  # sum denomenator series
        d1 += d * z

    H_abs = np.absolute(n1 / d1)  # frequency response
    ph_n = np.arctan(n1.imag / n1.real)
    ph_d = np.arctan(d1.imag / d1.real)
    H_phase = 180 * (ph_n - ph_d) / np.pi # phase response
    
    return H_abs, H_phase
```



## Plotting

The value of DPI (dots per inch) can be increased to save high definition plots to file:

```python
# to plot in hd
plt.figure(1, dpi=300)
# to save a figure in hd
plt.savefig('fig/ecg_mit100.png', dpi=300)
```



## References

1. [Numpy API Reference](https://numpy.org/doc/stable/reference/index.html)
1. [Matplotlib API Reference](https://matplotlib.org/stable/api/index.html)
1. [Python audio signal processing with librosa](https://daehnhardt.com/blog/2023/03/05/python-audio-signal-processing-with-librosa/)
2. [Signal processing for sound file](https://math.umd.edu/~petersd/464/soundstretch.html)
3. [Zheng et. al., A 12-lead electrocardiogram database for arrhythmia research covering more than 10,000 patients](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7016169/)
4. [Graphing and analyzing ECG data (from wav files)](https://electrophys.wordpress.com/home/electrocardiography/graphing-and-analyzing-ecg-data/)
5. [Bjørn-Jostein Singstad, Norwegian Endurance Athlete ECG Database](https://www.researchgate.net/publication/361792570_Norwegian_Endurance_Athlete_ECG_Database)
6. [numpy.dtype.byteorder documentation](https://numpy.org/doc/stable/reference/generated/numpy.dtype.byteorder.html)
7. [PhysioNet documentation](https://physionet.org/physiotools/wag/header-5.htm)
8. [Python WFDB package](https://wfdb.readthedocs.io/en/latest/wfdb.html)

