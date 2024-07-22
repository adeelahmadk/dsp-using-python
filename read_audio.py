import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf
import pygame

FileName = 'sample.wav'
x, Fs = sf.read(FileName)
Info = sf.info(FileName)
Channels = Info.channels
Duration = Info.duration
Frames = Info.frames
Nsamples = len(x)
Ts = 1/Fs


def mono_to_stereo(x):
    x2 = []
    x2.append(x)
    x2.append(x)
    x3 = np.array(x2)
    x3 = x3.transpose()
    return x3


# If mono, convert to stereo
if Channels < 2:
    x = mono_to_stereo(x)
    FileName = 'sample2.wav'
    sf.write(FileName, x, Fs)

# Init the pygame mixer
pygame.mixer.init()
sound = pygame.mixer.Sound(FileName)

# Play sound
sound.play()

# wait for the sound to finish
pygame.time.wait(int(sound.get_length() * Ts))

# plot channels
t = np.linspace(start=0.0, stop=Duration-Ts, num=Nsamples)

plt.figure()
plt.clf()
plt.subplot(2,1,1)
plt.plot(t, x[:, 0], 'b')
plt.grid()
plt.xlabel('t (sec.)')
plt.ylabel('x(t)')
plt.title('left channel')

#plt.figure(2)
plt.subplot(2,1,2)
#plt.clf()
plt.plot(t, x[:, 1], 'r')
plt.grid()
plt.xlabel('t (sec.)')
plt.ylabel('x(t)')
plt.title('right channel')

plt.suptitle('Audio Signal')
plt.savefig('audio_channels.png')
plt.show()

