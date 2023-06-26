# Code Source: [https://www.rfwireless-world.com/source-code/Python/Spectral-analysis-in-Python.html]
# Library Imports  
# This code snippet is not working as of now. 26 June 2023. @Ravi Chandra Vedula

from scipy.fftpack import fft, ifft
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal


fc = 1000  # frequency of the carrier
N = 1e3
fs = 10*fc # sampling frequency with oversampling factor=10
time = np.arange(N) / fs
x = np.sin(2*np.pi*fc*time) # time domain signal (real number)
plt.figure()
plt.plot(time, x)
plt.xlabel('Time')
plt.ylabel('Signal amplitude')
plt.title('Time domain signal amplitude versus time samples')

N1 = 256 # FFT size
X1 = fft(x, N1) # N-point complex DFT, output contains DC at index 0

# calculate frequency bins with FFT
# Power spectral density (PSD) using FFT and absolute squared

df=fs/N1 # frequency resolution
sampleIndex = np.arange(start = 0,stop = N1) # raw index for FFT plot
f=sampleIndex*df # x-axis index converted to frequencies
PSD = abs(X1)**2
n1 = len(f)//2
n2 = len(PSD)//2
plt.figure()
plt.plot(f[1:n1], PSD[1:n2])
plt.xlabel('Frequency indices')
plt.ylabel('Signal power')
plt.title('Frequency domain signal power vs frequency indices')

# Power spectral density (PSD) using signal.welch

f1, Pxx_spec = signal.welch(x, fs, 'flattop', 512, scaling='spectrum')
plt.figure()
plt.semilogy(f1, np.sqrt(Pxx_spec))
plt.xlabel('Frequency (Hz)')
plt.ylabel('PSD')
plt.title('Power spectrum as per scipy.signal.welch function')
plt.show()
