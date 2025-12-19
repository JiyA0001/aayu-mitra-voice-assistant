import sounddevice as sd
import soundfile as sf
import numpy as np

# ===== HARDWARE CONFIG =====
# USB Microphone: card 2 (from arecord -l)
MIC_DEVICE_INDEX = 2

SAMPLE_RATE = 48000
CHANNELS = 1
DTYPE = "int16"


def record_voice(filename="input.wav", duration=5):
    """
    Records audio from the USB microphone using ALSA only.
    Safe for Raspberry Pi boot usage.
    """
    try:
        print(f"🎙️ Recording for {duration} seconds... Speak now!")

        audio = sd.rec(
            frames=int(duration * SAMPLE_RATE),
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            dtype=DTYPE,
            device=MIC_DEVICE_INDEX
        )

        sd.wait()

        sf.write(filename, audio, SAMPLE_RATE)
        print("✅ Voice recorded and saved as 'input.wav'")

    except Exception as e:
        print("❌ Error while recording:", e)
