from gtts import gTTS
# import playsound
import pygame
import os
import time

def speak_text(text, lang="hi", filename="reply.mp3"):
    """
    Convert text to speech and play it.
    :param text: Text to convert
    :param lang: Language code ('hi' for Hindi, 'en' for English)
    :param filename: Output MP3 file
    """
    try:
        tts = gTTS(text=text, lang=lang)
        tts.save(filename)
        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

        # Wait until playback is done
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

        pygame.mixer.music.unload()
        os.remove(filename)  # cleanup after playing
    except Exception as e:
        print(f"❌ Error in TTS: {str(e)}")
