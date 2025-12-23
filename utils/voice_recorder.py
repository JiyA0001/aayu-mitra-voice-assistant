import sounddevice as sd
from scipy.io.wavfile import write

# ✅ FORCE correct microphone
sd.default.device = 0   # USB Composite Device
sd.default.channels = 1
sd.default.samplerate = 48000

def record_voice(filename="input.wav", duration=6, fs=48000):
    """
    Records audio from microphone and saves it to a WAV file.
    """
    print(f"🎙️ Recording for {duration} seconds... Speak now!")

    try:
        recording = sd.rec(
            int(duration * fs),
            samplerate=fs,
            channels=1,
            dtype="int16"
        )

        sd.wait()
        write(filename, fs, recording)
        print(f"✅ Voice recorded and saved as '{filename}'")

    except Exception as e:
        print("❌ Error while recording:", e)
