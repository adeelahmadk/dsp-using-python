# Digital Signal Processing

This repository is intended to be an introduction to digital signal processing concepts. The included Python scripts are designed to provide a basic understanding about how common signal processing algorithms are used to perform operations on discrete time signals and systems. The code is just for the educational purposes and by no means is production-ready.

## Contents

| Topic                           | Program                | Description                                                  |
| ------------------------------- | ---------------------- | ------------------------------------------------------------ |
| Audio Processing                | `read_audio.py`        | read a `.wav` file, plot its left & right channels           |
|                                 | `noisy_audio.py`       | read a `.wav` file, add WGN to it, plot noisy signal, and save it to a new file |
|                                 | `chirp.py`             | create a chirp signal. play, plot and save as file.          |
| Biomedical Signal Processing    | `ecg.py`               | read ECG data from WFDB format file, unpack and plot it.     |
|                                 | `ecg_mit.py`           | read, unpack, and plot a 12-bit packed ECG file (MIT-BIH).   |
| Fourier Transform & Convolution | `dft.py`               | compute FFT using numpy.                                     |
|                                 | `convo.py`             | perform linear and circular convolution of two sequences using FFT with numpy. |
|                                 | `circ_zeropad_conv.py` | perform circular zero-padded convolution of two sequences using FFT. |
|                                 | `dct.py`               | write functions for DCT & inverse DCT and use on an example. |
|                                 | `dht.py`               | write functions for Discrete Heartly Transform (DHT) with example. |
|                                 | `fft_conv_perf.py`     | performance analysis of linear & zero-padded circular convolution. |
| Discrete Time Systems           | `diff_eq.py`           | calculate amplitude and phase response of a system with FFT & series methods. |
|                                 | `conv_overlap_save.py` | convolution of long sequence using overlap and save method.  |
|                                 | `conv_overlap_add.py`  | convolution of long sequence using overlap and add method    |
| Simple FIR Filters              | `fir_lpf1.py`          | First order FIR low-pass filter                              |
|                                 | `fir_lpf2.py`          | Second order FIR low-pass filter                             |
|                                 | `fir_hpf1.py`          | FIR high-pass filter                                         |
|                                 | `fir_bpf1.py`          | FIR band-pass filter                                         |
|                                 | `fir_bsf1.py`          | FIR band-stop filter                                         |
| Simple IIR Filters              | `iir_lpf1.py`          | IIR low-pass filter                                          |
|                                 | `iir_hpf1.py`          | IIR high-pass filter                                         |
|                                 | `iir_bpf1.py`          | IIR band-pass filter                                         |
|                                 | `iir_bsf1.py`          | IIR band-stop filter                                         |
| Windowed FIR Filters            | `window_fir_lpf1.py`   | FIR LPF using Hanning window ([Example#1](notes.md#Example-Windowed-LPF)) |



### Directories

All source code files are located in the project root. Moreover, there are other directories that serve different purposes:

- `data`: datasets and output files.
- `fig`: plots and figures saved as files.
- `docs`: reading material.

## Data Sources

1. [Sound Examples](https://www.dsprelated.com/freebooks/pasp/Sound_Examples.html)
2. [Will Two Do? Varying Dimensions in Electrocardiography: The PhysioNet/Computing in Cardiology Challenge 2021](https://physionet.org/content/challenge-2021/1.0.2/)
3. [The PhysioNet/Computing in Cardiology Challenge 2021](https://paperswithcode.com/dataset/physionet-challenge-2021)
4. [Yoo et. al., Standardized Database of 12-Lead Electrocardiograms...](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10209728/)
5. [Zheng et. al., A 12-lead electrocardiogram database for arrhythmia research covering more than 10,000 patients](https://figshare.com/collections/ChapmanECG/4560497/2)
5. [Norwegian Endurance Athlete ECG Database](https://physionet.org/content/norwegian-athlete-ecg/1.0.0/)
7. [MIT-BIH Arrhythmia database](https://www.physionet.org/content/mitdb/1.0.0/)

