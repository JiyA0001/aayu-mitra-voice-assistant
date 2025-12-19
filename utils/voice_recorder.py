import sounddevice as sd
import soundfile as sf

MIC_NAME = "USB Composite Device"
SAMPLE_RATE = 48000
CHANNELS = 1
DTYPE = "int16"


def record_voice(filename="input.wav", duration=5):
    try:
        print(f"🎙️ Recording for {duration} seconds... Speak now!")

        # Find the correct device by name
        devices = sd.query_devices()
        mic_index = None
        for i, d in enumerate(devices):
            if MIC_NAME in d["name"] and d["max_input_channels"] > 0:
                mic_index = i
                break

        if mic_index is None:
            raise RuntimeError("USB microphone not found")

        audio = sd.rec(
            int(duration * SAMPLE_RATE),
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            dtype=DTYPE,
            device=mic_index
        )

        sd.wait()
        sf.write(filename, audio, SAMPLE_RATE)
        print("✅ Voice recorded and saved as 'input.wav'")

    except Exception as e:
        print("❌ Error while recording:", e)
