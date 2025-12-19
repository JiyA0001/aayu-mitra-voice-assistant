import sounddevice as sd
from scipy.io.wavfile import write
import os

def record_voice(filename="input.wav", duration=10, fs=48000):
    """
    Records audio from microphone and saves it to a WAV file.
    :param filename: Output WAV file name
    :param duration: Duration of recording in seconds
    :param fs: Sample rate (48000 is standard for many USB mics)
    """
    print(f"🎙️ Recording for {duration} seconds... Speak now!")
    try:
        # Optimization: Set defaults to prevent buzzing/gain pumping
        sd.default.samplerate = fs
        sd.default.channels = 1
        sd.default.dtype = 'int16'
        sd.default.blocksize = 1024
        
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()  # Wait until recording is finished
        write(filename, fs, recording)
        print(f"✅ Voice recorded and saved as '{filename}'")
    except Exception as e:
        print(f"❌ Error while recording: {str(e)}")
