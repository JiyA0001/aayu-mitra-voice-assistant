from gtts import gTTS
import os
import time
import subprocess
import threading
import uuid

tts_lock = threading.Lock()
pygame_ready = False

def _init_pygame():
    global pygame_ready
    if pygame_ready:
        return
    try:
        import pygame
        pygame.mixer.init(frequency=48000, buffer=4096)
        pygame_ready = True
        print("✅ pygame mixer initialized")
    except Exception as e:
        print("⚠️ pygame init failed:", e)
        pygame_ready = False

def speak_text(text, lang="hi", filename=None):
    if not filename:
        filename = f"/tmp/reply_{uuid.uuid4().hex}.mp3"

    with tts_lock:
        try:
            tts = gTTS(text=text, lang=lang)
            tts.save(filename)

            if not os.path.exists(filename) or os.path.getsize(filename) == 0:
                print("❌ TTS file missing or empty")
                return

            # Try pygame first
            _init_pygame()
            if pygame_ready:
                try:
                    import pygame
                    pygame.mixer.music.load(filename)
                    pygame.mixer.music.play()
                    while pygame.mixer.music.get_busy():
                        time.sleep(0.1)
                    pygame.mixer.music.unload()
                    os.remove(filename)
                    return
                except Exception as e:
                    print("⚠️ pygame playback failed:", e)

            # Fallback to mpg123
            try:
                subprocess.run(
                    ["mpg123", "-q", filename],
                    check=True
                )
            except Exception as e:
                print("❌ mpg123 playback failed:", e)

        finally:
            try:
                if os.path.exists(filename):
                    os.remove(filename)
            except:
                pass
