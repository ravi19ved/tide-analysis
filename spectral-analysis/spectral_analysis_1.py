# Another code snippet for doing Spectral Analysis 
# Source Webpage Link: https://currents.soest.hawaii.edu/ocn_data_analysis/_static/Spectrum.html
# Date: 26 June 2023
# Author: Ravi Chandra Vedula

#Library Imports for spectral analysis
import numpy as np 
import matplotlib.pyplot as py

import scipy.stats as ss 

from pycurrents.num import spectra 

plt.rcParams['figure.dpi'] = 90


def datafaker(nt, dt = 1, freqs = None, color = 'w', amp = 1,
                complex = True, repeatable = True):
    
    """
    Generate fake data with optional sinusoids (all the same amplitude)
    and with red, white, or blue noise of arbitrary amplitude. 

    *nt* : number of points
    *dt* : time increment in arbitrary time units
    *freqs* : None, or a sequence of frequencies in cycles per unit time. 
    *color* : 'r', 'w', 'b'
    *amp* : amplitude of red, white, or blue noise
    *complex* : True, Flase
    *repeatable* : True, False

    Returns t, x 
    """
    if repeatable:
        np.random.seed(1)
    noise = np.random.randn(nt+1) + 1j * np.random.randn(nt+1)

    if color == 'r':
        noise = np.cumsum(noise) / 10
        noise -= noise.mean()
    elif color == 'b':
        noise = np.diff(noise)
    noise = noise[:nt]
    x = amp * noise

    t = np.arange(nt, dtype=float) * dt
    
    for f in freqs:
        sinusoid = np.exp(2 * np.pi * 1j * f * t)
        x += sinusoid
    if not complex:
        x = np.real(x)
        
    return t, x

# Defining spectrum1 function
def spectrum1(h, dt=1):
    """
    First cut at spectral estimation: very crude.
    
    Returns frequencies, power spectrum, and
    power spectral density.
    Only positive frequencies between (and not including)
    zero and the Nyquist are output.
    """
    nt = len(h)
    npositive = nt//2
    pslice = slice(1, npositive)
    freqs = np.fft.fftfreq(nt, d=dt)[pslice] 
    ft = np.fft.fft(h)[pslice]
    psraw = np.abs(ft) ** 2
    # Double to account for the energy in the negative frequencies.
    psraw *= 2
    # Normalization for Power Spectrum
    psraw /= nt**2
    # Convert PS to Power Spectral Density
    psdraw = psraw * dt * nt  # nt * dt is record length
    return freqs, psraw, psdraw



nt = 240

dt = 1/24 # 1 hour sample interval
tides = [24/12.42, 24/12]

t, h = datafaker(nt, dt=dt, freqs=tides, amp=1, 
                 color='r',
                 complex=False)
fig, ax = plt.subplots()
ax.plot(t, h)
ax.set_xlabel('days');


# Pick two data lengths as number of samples.  These will be used
# throughout the following examples.  They need to be quite large
# for the examples to work well.
n1 = 2400
n2 = 24000

dfkw = dict(dt=dt, freqs=tides, amp=1, color='r', complex=False)

t, h1 = datafaker(n1, **dfkw)
freqs1, ps1, psd1 = spectrum1(h1, dt=dt)

t, h2 = datafaker(n2, **dfkw)
freqs2, ps2, psd2 = spectrum1(h2, dt=dt)

fig, axs = plt.subplots(ncols=2, sharex=True)
axs[0].loglog(freqs1, psd1, 'r',
              freqs2, psd2, 'b', alpha=0.5)
axs[1].loglog(freqs1, ps1, 'r', 
              freqs2, ps2, 'b', alpha=0.5)
axs[0].set_title('Power Spectral Density')
axs[1].set_title('Power Spectrum')
axs[1].axis('tight', which='x');

print('PS sum:   %.2f, %.2f' % (ps1.sum(), ps2.sum()))
print('Variance: %.2f, %.2f' % (h1.var(), h2.var()))
print('Differences: %g, %g' % (h1.var() - ps1.sum(),
                               h2.var() - ps2.sum()))


print('Tidal peak')

# Find a small band centered on the tidal constituents:
cond1 = (freqs1 < 24/11) & (freqs1 > 24/13.5) 
df1 = 1 / (len(h1) * dt)
psdint1 = psd1[cond1].sum() * df1

cond2 = (freqs2 < 24/11.9) & (freqs2 > 24/12.52) 
df2 = 1 / (len(h2) * dt)
psdint2 = psd2[cond2].sum() * df2

print('PSD integral:%.2f, %.2f' % (psdint1, psdint2))

print('PS tidal max: %.2g, %.2g' % (ps1[cond1].max(),
                                    ps2[cond2].max()) )
print('PSD tidal max: %.2g, %.2g' % (psd1[cond1].max(),
                                    psd2[cond2].max()) )


def spectrum2(h, dt=1, nsmooth=5):
    """
    Add simple boxcar smoothing to the raw periodogram.
    
    Chop off the ends to avoid end effects.
    """
    freqs, ps, psd = spectrum1(h, dt=dt)
    weights = np.ones(nsmooth, dtype=float) / nsmooth
    ps_s = np.convolve(ps, weights, mode='valid')
    psd_s = np.convolve(psd, weights, mode='valid')
    freqs_s = np.convolve(freqs, weights, mode='valid')
    return freqs_s, ps_s, psd_s

dfkw = dict(dt=dt, freqs=tides, amp=1, color='r', complex=False)

t, h1 = datafaker(n1, **dfkw)
freqs1, ps1, psd1 = spectrum2(h1, dt=dt)

t, h2 = datafaker(n2, **dfkw)
freqs2, ps2, psd2 = spectrum2(h2, dt=dt)

fig, axs = plt.subplots(ncols=2, sharex=True)
axs[0].loglog(freqs1, psd1, 'r',
              freqs2, psd2, 'b', alpha=0.5)
axs[1].loglog(freqs1, ps1, 'r', 
              freqs2, ps2, 'b', alpha=0.5)
axs[0].set_title('Power Spectral Density')
axs[1].set_title('Power Spectrum')
axs[1].axis('tight', which='x');

def spectrum3(h, dt=1, nsmooth=5):
    """
    Detrend first.
    """
    t = np.arange(len(h))
    p = np.polyfit(t, h, 1)
    h_detrended = h - np.polyval(p, t)
    return spectrum2(h_detrended, dt=dt, nsmooth=nsmooth)



