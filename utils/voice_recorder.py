import sounddevice as sd
from scipy.io.wavfile import write
import os

def record_voice(filename="input.wav", duration=10, fs=44100):
    """
    Records audio from microphone and saves it to a WAV file.
    :param filename: Output WAV file name
    :param duration: Duration of recording in seconds
    :param fs: Sample rate (44100 is CD quality)
    """
    print(f"🎙️ Recording for {duration} seconds... Speak now!")
    try:
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()  # Wait until recording is finished
        write(filename, fs, recording)
        print(f"✅ Voice recorded and saved as '{filename}'")
    except Exception as e:
        print(f"❌ Error while recording: {str(e)}")
