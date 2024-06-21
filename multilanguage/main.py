import speech_recognition as sr
import pyttsx3
import pyaudio
import wave

# Konuşma tanıma motorlarını ve seslendirme motorunu kurun
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Ses girişi ayarlarını yapılandırın
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

while True:
    # Kullanıcıdan dil seçmesini isteyin
    print("Lütfen konuşulan dili seçin (de, en, tr): ")
    dil = input().lower()

    # Ses girişini alın
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    print("Dinleniyor...")

    frames = []
    for i in range(0, int(RATE / CHUNK * 5)):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Ses girişini kaydedin ve konuşmayı metne dönüştürün
    with wave.open("output.wav", "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b"".join(frames))

    with sr.AudioFile("output.wav") as source:
        audio_data = recognizer.record(source)

    # Konuşmayı metne dönüştürün
    try:
        if dil == "de":
            text = recognizer.recognize_google(audio_data, language="de-DE")
        elif dil == "en":
            text = recognizer.recognize_google(audio_data, language="en-US")
        elif dil == "tr":
            text = recognizer.recognize_google(audio_data, language="tr-TR")
        else:
            print("Geçersiz dil seçimi.")
            continue
    except sr.UnknownValueError:
        print("Ses tanınamadı.")
        continue
    except sr.RequestError as e:
        print("Google Speech-to-Text hizmeti hatası; {0}".format(e))
        continue

    print("Söylediğiniz: {}".format(text))

    # İstediğiniz işlemleri yapın
    # Örneğin, metni sesli olarak okuyabiliriz
    engine.say(text)
    engine.runAndWait()
