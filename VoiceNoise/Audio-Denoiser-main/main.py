import numpy as np
import matplotlib.pyplot as plt
import matplotlib.style as style
#from scipy.io import wavfile
import noisereduce as nr
import wave

style.use('ggplot')

# WAV dosyasını okuma
file_path = "input.wav"

# wave kütüphanesi ile dosyayı açma ve bilgileri okuma
with wave.open(file_path, 'rb') as wf:
    rate = wf.getframerate()
    frames = wf.readframes(wf.getnframes())
    num_channels = wf.getnchannels()
    sample_width = wf.getsampwidth()

# NumPy dizisine dönüştürme
data = np.frombuffer(frames, dtype=np.int16)

# Gürültüyü azaltma
#reduced_noise = nr.reduce_noise(y=data, sr=rate)
reduced_noise = nr.reduce_noise(y=data, sr=rate, prop_decrease=0.6, time_constant_s=5, freq_mask_smooth_hz=500)

# Orijinal ve gürültü azaltılmış sinyalleri çizme
fig, ax = plt.subplots(2, 1, figsize=(15, 8))
ax[0].set_title("Original signal")
ax[0].plot(data)
ax[1].set_title("Reduced noise signal")
ax[1].plot(reduced_noise)
plt.show()

# Gürültü azaltılmış sinyali WAV dosyasına kaydetme
output_path = "output.wav"

# wave kütüphanesi ile dosyayı kaydetme
with wave.open(output_path, 'wb') as wf:
    wf.setnchannels(num_channels)
    wf.setsampwidth(sample_width)
    wf.setframerate(rate)
    wf.writeframes(reduced_noise.astype(np.int16).tobytes())

print(f"Reduced audio saved to {output_path}")
