from gtts import gTTS
import pygame
import os
import time
import subprocess
import threading
import uuid

os.environ["SDL_AUDIODRIVER"] = "alsa"

pygame.mixer.pre_init(frequency=48000, size=-16, channels=2, buffer=2048)
pygame.mixer.init()

tts_lock = threading.Lock()

def speak_text(text, lang="hi", filename=None):
    if not filename:
        filename = f"reply_{uuid.uuid4().hex}.mp3"

    with tts_lock:
        try:
            tts = gTTS(text=text, lang=lang)
            tts.save(filename)

            if not os.path.exists(filename) or os.path.getsize(filename) == 0:
                print("TTS file generation failed")
                return

            try:
                pygame.mixer.music.load(filename)
                pygame.mixer.music.play()

                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)

            except Exception as e:
                print("Pygame failed, trying mpg123:", e)
                subprocess.run(["mpg123", "-q", filename], check=False)

            finally:
                try:
                    if os.path.exists(filename):
                        os.remove(filename)
                except:
                    pass

        except Exception as e:
            print("TTS error:", e)
