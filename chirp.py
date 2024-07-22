import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf
from playsound import playsound
import math


def mono_to_stereo(x):
    x2 = []
    x2.append(x)
    x2.append(x)
    x3 = np.array(x2)
    x3 = x3.transpose()
    return x3


def play_sound(file_name):
    import pygame
    # Init the pygame mixer
    pygame.mixer.init()
    sound = pygame.mixer.Sound(file_name)
    # Play sound
    sound.play()
    # wait for the sound to finish
    pygame.time.wait(int(sound.get_length() * Ts))


lambda1 = 1000
Fs = 8000
f0 = 1000
Ts = 1/Fs
Duration = 2.0 # sec.
Nsamples = int(Duration / Ts)
t = np.arange(0.0, Duration - Ts, Ts)
theta = (2 * np.pi * f0 * t) + (np.pi * lambda1 * np.power(t, 2))

#CosData = []
#for nT in range(len(theta)):
#    CosData.append(0.1 * math.cos(theta[nT]))

CosData = 0.1 * np.cos(theta)

# convert to stereo
x = mono_to_stereo(CosData)
FileName = 'data/output/chirp_sound.wav'
sf.write(FileName, x, Fs)

playsound(FileName)

# plot channels
plt.figure(1)
plt.clf()
plt.plot(t, x[:, 0], 'b')
plt.grid()
plt.ylabel('t (sec.)')
plt.ylabel('x(t)')
plt.title('Audio Signal')

plt.savefig('fig/chirp_sound_signal.png')

plt.show()

