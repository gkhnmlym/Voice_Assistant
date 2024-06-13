import os
import pyaudio
import wave
import json
from vosk import Model, KaldiRecognizer
from gtts import gTTS

# Speech-to-Text için Vosk modelini yükleyin
if not os.path.exists("model"):
    print("Vosk model dosyası bulunamadı. Modeli 'model' klasörüne indirin.")
    exit(1)

model = Model("model")

def record_audio(filename):
    chunk = 1024
    sample_format = pyaudio.paInt16
    channels = 1
    rate = 16000
    seconds = 5
    p = pyaudio.PyAudio()
    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=rate,
                    frames_per_buffer=chunk,
                    input=True)
    frames = []

    print("Recording...")
    for _ in range(0, int(rate / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)

    print("Recording complete")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()


def speech_to_text(filename):
    wf = wave.open(filename, "rb")
    recognizer = KaldiRecognizer(model, wf.getframerate())
    recognizer.SetWords(True)
    text = ""

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            result_json = json.loads(result)
            text += result_json.get("text", "")

    result = recognizer.FinalResult()
    result_json = json.loads(result)
    text += result_json.get("text", "")

    print("Transcript: {}".format(text))
    return text


def text_to_speech(text, output_filename):
    tts = gTTS(text=text, lang='en')
    tts.save(output_filename)
    print('Audio content written to file "{}"'.format(output_filename))


def main():
    audio_filename = "input.wav"
    text_filename = "speech.txt"
    response_audio_filename = "response.mp3"

    record_audio(audio_filename)
    text = speech_to_text(audio_filename)

    if text:
        with open(text_filename, "w") as file:
            file.write(text)

        user_input = input("Do you want to hear the text read out loud? (yes/no): ")
        if user_input.lower() in ['yes', 'y']:
            with open(text_filename, "r") as file:
                text_to_read = file.read()
            text_to_speech(text_to_read, response_audio_filename)
            print("Playing the response...")
            os.system("start " + response_audio_filename)  # Windows
            # os.system("afplay " + response_audio_filename)  # MacOS
            # os.system("mpg123 " + response_audio_filename)  # Linux


if __name__ == "__main__":
    main()
