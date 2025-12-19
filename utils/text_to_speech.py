from gtts import gTTS
import subprocess
import os
import uuid
import platform

def speak_text(text, lang="en"):
    base = f"/tmp/reply_{uuid.uuid4().hex}"
    mp3 = base + ".mp3"
    wav = base + ".wav"

    try:
        tts = gTTS(text=text, lang=lang)
        tts.save(mp3)

        system = platform.system()

        if system == "Linux":
            # Convert to wav and play via ALSA
            subprocess.run(
                ["ffmpeg", "-y", "-loglevel", "quiet", "-i", mp3, wav],
                check=True
            )
            subprocess.run(
                ["aplay", "-q", wav],
                check=True
            )

        elif system == "Windows":
            # Simple playback on Windows
            from playsound import playsound
            playsound(mp3)

        else:
            print("Unsupported OS for audio playback")

    except Exception as e:
        print("TTS ERROR:", e)

    finally:
        for f in [mp3, wav]:
            try:
                if os.path.exists(f):
                    os.remove(f)
            except:
                pass
