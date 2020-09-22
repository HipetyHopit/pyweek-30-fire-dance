"""@package beatTracking

Track beats.
"""

import numpy as np
from scipy.io import wavfile
from scipy.signal import decimate, find_peaks
from constants import *

logCompress = lambda x: np.log(1 + GAMMA*abs(x))
halfWaveRect = lambda x: (x + abs(x))/2.

def spectrogram(x, N = N, H = H, K = K, w = np.blackman):
    """
    Return the spectrogram of a signal x.

    Keyword arguments:
    x -- the input signal.
    N -- the window size. (default = N)
    H -- the hop size. (default = H)
    K -- half the FFT size. (default = K)
    w -- the window function. (default = np.blackman)

    Returns:
    X -- the spectrogram transform of x.
    """
    
    # Pad
    x = np.append(np.zeros(N//2), x)
    x = np.append(x, np.zeros(N//2))
    
    T = (len(x)-N)//H
    
    if (K == None or K < N//2):
        K = N//2
    
    X = np.empty((T, K), dtype = np.complex_)
    
    # Window
    w = w(N)
    
    for t in range(T):
        xt = x[t*H:(t*H + N)]
        xt = np.append(xt*w, np.zeros(2*K - N))
        X[t] = np.fft.fft(xt)[:K]
    
    return X

def temporalDerivative(X):
    """
    Return the temporal derivative of a spectrogram.
    
    Keyword arguments:
    X -- the input spectrogram

    Returns:
    delta -- the specral-based novelty function.
    """
    
    T = X.shape[0]
    K = X.shape[1]
    
    delta = np.zeros(T)
    X = np.append(X, np.zeros((1, K)), axis = 0)
    
    for t in range(T):
        for k in range(K):
            delta[t] += halfWaveRect(X[t+1][k] - X[t][k])
    
    return delta

def localAverage(x, M):
    """
    Return the local average of a signal.

    Keyword arguments:
    x -- the input signal.
    M -- the averaging window size.

    Returns:
    mu -- the spectrogram transform of s.
    """
    
    mu = np.zeros(len(x))
    
    for n in range(len(x)):
        for m in range(0 if n < M else n-M, 
                       len(x) if n + M > len(x) else n + M):
            mu[n] += x[m]
        
    mu /= 2*M + 1
    
    return mu

def loadWav(f):
    """
    Load a .wav file.
    
    Keyword arguments:
    f -- the file to load.
    
    Returns:
    x -- the raw audio.
    Fs -- the sampling frequency.
    """
    
    Fs, x = wavfile.read(f)
    
    if (len(x.shape) > 1):
        x = np.mean(x, axis = 1)
        
    if (Fs > 22050):
        x = decimate(x, 2)
    
    return x, Fs

def getMoves(track = "disco.00000.wav", levels = 2, interval = 1.):
    """
    Return an array of beat positions at which moves should occur.
    
    Keyword arguments:
    track -- the file name of the track for which to generate moves.
        (default  = "disco.00000.wav") 
    levels -- the number of increasing levels of granulity to 
        generate moves for. (default = 2) 
    interval -- th minimum interval between level 1 moves (s). 
        (default = 1.) 
        
    Returns:
    moves -- an array of move positions in time (s).
    """
    
    x, Fs = loadWav(SONGS_PATH + track)
    
    X = abs(spectrogram(x))
    novelty = temporalDerivative(logCompress(X))
    mu = localAverage(novelty, 100)
    novelty = halfWaveRect(novelty - mu)
    
    moves = []
    
    for i in range(levels):
        moves += find_peaks(novelty, 
                            distance = int(interval*Fs/(H*levels)))*H/Fs
        
    return moves

if (__name__ == "__main__"):
    
    import matplotlib.pyplot as plt
    import matplotlib
    
    x, Fs = loadWav("songs/disco.00000.wav")
    #x, Fs = loadWav("songs/Clara Berry And Wooldog - Air Traffic.stem.wav")
    
    x = x#[:Fs*3]
    
    # Plot waveform.
    
    t = np.arange(len(x))/Fs
    
    #fig = plt.figure()
    #ax = plt.subplot(111)
    #ax.set_xlim(t[0], t[-1])
    #ax.plot(t, x)
    #plt.show()
    
    # Plot spectorgram.
    
    X = abs(spectrogram(x))
    
    #fig = plt.figure()
    #ax = plt.subplot(111)
    #ax.imshow(20*np.log(X).T, cmap = "Blues", origin = "lower", aspect = "auto")
    #plt.show()
    
    # Plot novelty function.
    
    novelty = temporalDerivative(logCompress(X))
    mu = localAverage(novelty, 100)
    t = np.arange(len(X))*H/Fs
    
    #fig = plt.figure()
    #ax = plt.subplot(111)
    #ax.set_xlim(t[0], t[-1])
    #ax.plot(t, novelty)
    #ax.plot(t, mu)
    #plt.show()
    
    # Plot improved novelty function.
    
    novelty = halfWaveRect(novelty - mu)
    
    fig = plt.figure()
    ax = plt.subplot(111)
    ax.set_xlim(t[0], t[-1])
    ax.plot(t, novelty)
    plt.show()
 
    # Plot onsets.
    
    peaks = find_peaks(novelty, distance = int(0.5*Fs/H))
    
    t = np.arange(len(x))/Fs
    
    fig = plt.figure()
    ax = plt.subplot(111)
    ax.set_xlim(t[0], t[-1])
    ax.plot(t, x)
    
    ax.vlines(peaks[0]*H/Fs, x.min(), x.max())
    
    plt.show()
