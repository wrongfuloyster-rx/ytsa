from __future__ import unicode_literals
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy.io import wavfile
import numpy as np
import youtube_dl


target_url = 'https://www.youtube.com/watch?v=y-BFrPQPGjM'

ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl' : 'ex_audio.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav',
#        'preferredquality': '192',
        }],
}

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([target_url])

rate, audio = wavfile.read('ex_audio.wav') #read the wav file, 'fs' not used
audio = np.float32(np.mean(audio, axis=1))
#audio = audio.T[0] #take only one of the two (stereo) audio channels
n_samples = len(audio)
duration = n_samples / rate
audio_freq = fft(audio) #calculates the fourier transform
audio_freq_real = round(len(audio_freq)/2) #(not used) in case you want to display the real symmetry
#signal = audio_freq[0:-1] #replace number with 'd', otherwise used as a freq filter
signal = abs(audio_freq[0:(audio_freq_real-1)])

print(f'Audio length: {duration:.2f} seconds')
print(audio_freq_real)

fig, (axis1, axis2) = plt.subplots(1,2)
fig.suptitle("WAV File Analysis")
axis1.plot(np.arange(n_samples) / rate, audio)
axis1.set_xlabel('Times [S]')
axis1.set_ylabel('Amplitude [Unknown]')

axis2.plot(signal,'r') #plot the absolute value of the 'signal' array, use a red line
axis2.set_xlabel('Sample Number')
axis2.set_ylabel('Amplitude [dB]')

plt.show() #show the plot

np.savetxt("training set/ex_audio.txt", np.array(audio_freq), fmt="%s")
