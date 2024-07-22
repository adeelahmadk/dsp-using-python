import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf
import pygame

FileName = 'data/wave/sample.wav'
x, Fs = sf.read(FileName)
Info = sf.info(FileName)
Channels = Info.channels
Duration = Info.duration
Frames = Info.frames
Nsamples = len(x)
Ts = 1/Fs

def mono_to_stereo(s):
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


# Add noise
def add_noise(s, samples, amp=1.0):
    noise_L = amp * np.random.normal(0, 1, samples)
    noise_R = amp * np.random.normal(0, 1, samples)

    tmpL = s[:,0] + noise_L
    tmpR = s[:,1] + noise_R
    tmp3 = []
    tmp3.append(tmpL)
    tmp3.append(tmpR)
    corrupted_signal = np.array(tmp3)
    return corrupted_signal


NoiseAmp = 0.01
corrupted_x = add_noise(x, Nsamples, amp=NoiseAmp)
FileName2 = 'data/output/corrupted_audio.wav'
sf.write(FileName2, corrupted_x, Fs)

# Play noisy sound
pygame.mixer.init()
sound2 = pygame.mixer.Sound(FileName2)
sound2.play()
pygame.time.wait(int(sound.get_length() * Ts))

# plot channels
t = np.linspace(start=0.0, stop=Duration-Ts, num=Nsamples)

plt.figure(1)
plt.clf()
plt.subplot(2,1,1)
plt.plot(t, x[:, 0], 'b')
plt.grid()
plt.ylabel('x(t)')
plt.title('left channel')

plt.subplot(2,1,2)
plt.plot(t, x[:, 1], 'r')
plt.grid()
plt.xlabel('t (sec.)')
plt.ylabel('x(t)')
plt.title('right channel')
plt.suptitle('Audio Signal')

plt.figure(2)
plt.plot(t, noise_L, 'r')
plt.grid()
plt.xlabel('t (sec.)')
plt.ylabel('n(t)')
plt.title('AWGN')
plt.savefig('awgn.png')

plt.figure(3)
plt.plot(t, corrupted_x, 'g')
plt.grid()
plt.xlabel('t (sec.)')
plt.ylabel('x(t) + n(t)')
plt.title('Audio Signal corrupted with AWGN')
plt.savefig('audio_with_awgn.png')

plt.show()

