import threading
import datetime
import time
import traceback
from collections import deque

from utils.voice_recorder import record_voice
from utils.transcriber_sr import transcribe_audio_sr
from llm.emotion_model import get_emotional_reply
from config import LLM_MODE
from utils.text_to_speech import speak_text
from utils.context_logger import log_message
from utils.device_id import get_device_id

import utils.aayu_firebase as firebase

from features.reminders import check_reminders, reminder_loop
from features.sos import detect_sos, trigger_emergency_alert


def detect_language(text: str) -> str:
    for ch in text:
        if '\u0900' <= ch <= '\u097F':
            return "hi"
    return "en"


def main():
    print("DEBUG main started")

    try:
        firebase.init_db()
        print("DEBUG Firestore initialized")
    except Exception as e:
        print("WARNING Firestore init failed", e)

    PI_ID = get_device_id()
    print("DEBUG Device PI_ID:", PI_ID)

    # Start reminder thread
    try:
        reminder_thread = threading.Thread(
            target=reminder_loop,
            daemon=True
        )
        reminder_thread.start()
        print("DEBUG Reminder thread started")
    except Exception as e:
        print("WARNING Reminder thread failed", e)

    # ---- GREETING ----
    try:
        print("DEBUG About to speak greeting")
        time.sleep(3)
        speak_text("Hello I am Aayu Mitra. How can I help you today?", lang="en")
        print("DEBUG Greeting finished")
    except Exception as e:
        print("ERROR Greeting failed", e)

    # Let playback fully complete before mic opens
    time.sleep(1)

    conversation_history = deque(maxlen=5)

    while True:
        try:
            print("DEBUG Waiting for user input")

            record_voice(filename="input.wav", duration=5)

            text = transcribe_audio_sr("input.wav", language="en-IN")

            if not text:
                print("DEBUG No transcription")
                continue

            print("USER:", text)
            try:
                log_message("user", text)
            except Exception:
                pass

            if detect_sos(text):
                print("DEBUG SOS detected")
                trigger_emergency_alert(text)
                continue

            detected_lang = detect_language(text)

            reply = get_emotional_reply(
                text,
                lang=detected_lang,
                mode=LLM_MODE,
                history=list(conversation_history)
            )

            conversation_history.append((text, reply))
            print("ASSISTANT:", reply)

            try:
                log_message("assistant", reply)
            except Exception:
                pass

            speak_text(reply, lang=detected_lang)

            time.sleep(0.5)

        except KeyboardInterrupt:
            print("DEBUG Keyboard interrupt")
            break
        except Exception as e:
            print("ERROR in main loop", e)
            traceback.print_exc()
            time.sleep(1)


if __name__ == "__main__":
    main()
