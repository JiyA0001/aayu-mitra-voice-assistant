from gtts import gTTS
import pygame
import os
import time
import subprocess
import threading
import uuid

# Global lock to prevent overlapping audio
tts_lock = threading.Lock()

def speak_text(text, lang="hi", filename=None):
    """
    Convert text to speech and play it.
    Uses pygame as primary player, falls back to mpg123 (CLI) if available.
    Thread-safe: blocks until previous audio finishes.
    """
    # Use a unique filename if none provided to prevent collisions
    if not filename:
        filename = f"reply_{uuid.uuid4().hex}.mp3"
        
    with tts_lock:
        try:
            tts = gTTS(text=text, lang=lang)
            tts.save(filename)
            
            # Verify file exists and has content
            if not os.path.exists(filename) or os.path.getsize(filename) == 0:
                print("❌ TTS Error: Audio file generation failed (empty or missing).")
                return

            # Try pygame first
            try:
                if not pygame.mixer.get_init():
                    pygame.mixer.init(frequency=24000, buffer=4096)
                
                pygame.mixer.music.load(filename)
                pygame.mixer.music.play()
                
                # Give it a moment to start
                time.sleep(0.2)
                
                # Wait until playback is done
                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)
                    
                pygame.mixer.music.unload()
                
            except Exception as e:
                print(f"⚠️ Pygame TTS failed, trying fallback: {e}")
                # Fallback to mpg123 (common on Linux/Pi)
                try:
                    subprocess.run(["mpg123", "-q", filename], check=True)
                except Exception as e2:
                    print(f"❌ Fallback TTS failed: {e2}")

            # Cleanup
            if os.path.exists(filename):
                try:
                    os.remove(filename)
                except PermissionError:
                    pass # File might still be in use, ignore
                    
        except Exception as e:
            print(f"❌ Error in TTS generation: {str(e)}")
