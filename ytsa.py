# ytsa.py
#
# This script downloads a youtube video file, strips the audio from it, performs an FFT
# and then plots the timeseries and FFT results.  The FFT array is then stored in a file
# for future projects.
#
# written by WrongfulOyster, September 2019. leveraging great work by youtube-dl
#
# requires:  scipy.fftpack, scipy.io, matplotlib, numpy, youtube-dl, ffmpeg


from __future__ import unicode_literals
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy.io import wavfile
import numpy as np
import youtube_dl

#makes the YouTube link highly visible - copy/paste the link to the desired video
target_url = 'https://www.youtube.com/watch?v=y-BFrPQPGjM'

#configure the youtube_dl options
ydl_opts = {
    'format': 'bestaudio/best',  #requests the best audio available for that video
    'outtmpl' : 'ex_audio.%(ext)s',  #save aduaio file as... "exaudio.wav"
    'postprocessors': [{
        'key': 'FFmpegExtractAudio', #use FFmpeg to strip the audio from the video
        'preferredcodec': 'wav', #save as .wav file
        }],
}

#leverage youtube_dl do download the video, passes the target URL and configuration options
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([target_url])

## Perform an FFT on the audio file

rate, audio = wavfile.read('ex_audio.wav') #read the wav file, stores data to "audio" and rate as "rate"
audio = np.float32(np.mean(audio, axis=1)) #takes both stereo channels and makes a mono channel

n_samples = len(audio) #determine the length of the audio file (number of samples)
duration = n_samples / rate #determine the duration of yje file in seconds
audio_freq = fft(audio) #calculates the fourier transform
audio_freq_real = round(len(audio_freq)/2) #Only show the _real_ portions of the aduio file
#signal = audio_freq[0:-1] #replace number with 'd', otherwise used as a freq filter
signal = abs(audio_freq[0:(audio_freq_real-1)]) #timeseries data

print(f'Audio length: {duration:.2f} seconds')
print(audio_freq_real)

fig, (axis1, axis2) = plt.subplots(1,2)  #sets up a signal display w/ 2 plots (horiz.)
fig.suptitle("WAV File Analysis") #Window title
axis1.plot(np.arange(n_samples) / rate, audio) #plot the timeseries
axis1.set_xlabel('Times [S]')
axis1.set_ylabel('Amplitude [Unknown]')

axis2.plot(signal,'r') #plot the frequency domain
axis2.set_xlabel('Sample Number')
axis2.set_ylabel('Amplitude [dB]')

plt.show() #show the plot

np.savetxt("training set/ex_audio.txt", np.array(audio_freq), fmt="%s") #store FFT array for future reference
