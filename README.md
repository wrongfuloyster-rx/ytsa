# YouTube Spectrum Analyzer (ytsa)

## Introduction

This script downloads a YouTube video file, strips the audio from it, performs an FFT on the WAV file, and then plots both the timeseries and FFT results. The FFT array is then stored in a file for later/future projects.

## Dependencies

YTSA requires the following packages to be installed:

+ matplotlib.pyplot
+ scipy.fftpack
+ scipy.io
+ numpy
+ youtube_dl
+ FFmpeg
