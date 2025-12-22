import warnings
# Suppress pygame pkg_resources deprecation warning
warnings.filterwarnings("ignore", category=UserWarning, module="pygame")

# from utils.voice_recorder import record_voice
# from utils.transcriber_whisper import transcribe_audio_whisper, transcribe_audio_whisper_dynamic
# from llm.emotion_model import get_emotional_reply
# from config import LLM_MODE
# from utils.text_to_speech import speak_text
# from utils.transcriber_sr import transcribe_audio_sr
# from utils.context_logger import log_message
# from features.reminders import check_reminders, reminder_loop
# from features.sos import detect_sos, trigger_emergency_alert
# import threading


# def detect_language(text: str) -> str:
#     for char in text:
#         if '\u0900' <= char <= '\u097F':
#             return 'hi'  # Hindi
#     return 'en'  # Default to English


# def select_language():
#     choice = input("🗣️ Speak in [1] Hindi or [2] English? (1/2): ")
#     return "hi-IN" if choice.strip() == "1" else "en-IN"

# def main():
#     print("🎙️ Starting Elderly Voice Assistant (Speech → LLM)")
#     cmd = input("\nPress [Enter] to speak or type 'q' to quit: ")
#     # if cmd.lower() == 'q':
#     #     break

#     lang = select_language()
#     # ✅ Step 0: Start the background reminder thread
#     reminder_thread = threading.Thread(target=reminder_loop, daemon=True)
#     reminder_thread.start()

#     while True:
#         reminder_message = check_reminders()
#         if reminder_message:
#             print("🔔 Reminder:", reminder_message)
#             speak_text(reminder_message)
            

#         # Step 1: Record audio
#         record_voice(filename="input.wav", duration=6)

#         # Step 2: Transcribe
#         # text = transcribe_audio_whisper("input.wav", language=lang)  # auto-detect language
#         text = transcribe_audio_sr("input.wav", language=lang)  # auto-detect language
#         # text = transcribe_audio_sr("input.wav")  # auto-detect language
#         print(f"📄 You said: {text}")
#         log_message("user", text)
#         # text, lang = transcribe_audio_whisper_dynamic("input.wav")
#         # print("📄 You said:", text)

#         if detect_sos(text):
#             trigger_emergency_alert(text)
        
#         # Step 3: Detect language
#         lang = detect_language(text)

#         # Step 4: Get emotional reply
#         reply = get_emotional_reply(text, lang=lang, mode=LLM_MODE)  # or "openai"
#         print(f"🤖 Assistant: {reply}")
#         log_message("assistant", reply)
#         speak_text(reply, lang=lang)  # 'hi' or 'en'

# if __name__ == "__main__":
#     main()





# main_voice_loop.py
import threading
import datetime
import time
# import winsound
import traceback
from collections import deque

from utils.voice_recorder import record_voice
from utils.transcriber_sr import transcribe_audio_sr
from llm.emotion_model import get_emotional_reply
from config import LLM_MODE
from utils.text_to_speech import speak_text
from utils.context_logger import log_message      # local logger (jsonl)
from utils.device_id import get_device_id

# Firestore helpers from the file you provided
import utils.aayu_firebase as firebase

# features (in-memory fallback)
# from features.reminders import check_reminders, reminder_loop
from features.sos import detect_sos, trigger_emergency_alert

# ---- simple unicode-based language detector ----
def detect_language(text: str) -> str:
    for ch in text:
        if '\u0900' <= ch <= '\u097F':
            return 'hi'
    return 'en'


def select_language():
    choice = input("🗣️ Speak in [1] Hindi or [2] English? (1/2): ")
    return "hi-IN" if choice.strip() == "1" else "en-IN"

# ---- Fallback / Demo Data ----
DEMO_PROFILE = {
    "name": "Smt. Saraswati",
    "age": 74,
    "notes": "Hears well with hearing aid, prefers Hindi",
    "sleep_schedule": {"planned_bedtime": "22:00", "planned_wakeup": "06:00"}
}

# ---- Firestore-backed reminder query & mark-complete helpers (uses DATA_ROOT from your module) ----
def db_reminder_loop(pi_id: str, poll_interval: int = 60):
    print(f"🔁 Firestore reminder loop started for {pi_id} (poll {poll_interval}s)")
    while True:
        try:
            now = datetime.datetime.now().strftime("%H:%M")
            # Use the new utility function
            due = firebase.get_due_reminders(pi_id, now)
            for r in due:
                msg = r.get("message") or r.get("label") or "Reminder"
                print("🔔 DB Reminder:", msg)
                try:
                    # choose language for reminder (this can be improved using user_pref)
                    speak_text(msg, lang="hi")
                except Exception as e:
                    print("TTS error while speaking reminder:", e)
                # mark completed so it won't repeat
                try:
                    firebase.mark_reminder_completed(pi_id, r["id"])
                except Exception as e:
                    print("Failed to mark reminder completed:", e)
            time.sleep(poll_interval)
        except Exception as e:
            print("⚠️ Error in db_reminder_loop:", e)
            traceback.print_exc()
            time.sleep(poll_interval)

# ---- main loop ----
def main():
    print("🎙️ Starting Elderly Voice Assistant (Speech → LLM)")

    # initialize Firestore (will raise helpful errors if credentials / APP_ID missing)
    try:
        firebase.init_db()
        # try:
        #     winsound.Beep(1000, 200)   # frequency=1000 Hz, duration=200 ms
        # except:
        #     pass
        print("✅ Firestore initialized (DATA_ROOT =", firebase.DATA_ROOT, ")")
    except Exception as e:
        print("⚠️ Firestore init failed — proceed in local/demo mode. Error:", e)

    PI_ID = get_device_id()
    print("Device PI_ID:", PI_ID)

    # Start background reminder thread using Firestore (preferred)
    try:
        reminder_thread = threading.Thread(target=db_reminder_loop, args=(PI_ID,), daemon=True)
        reminder_thread.start()
    except Exception as e:
        print("⚠️ Could not start Firestore reminder loop:", e)
        # Fallback removed as per new requirement to only use Firestore
        # try:
        #     reminder_thread = threading.Thread(target=reminder_loop, daemon=True)
        #     reminder_thread.start()
        # except Exception as e2:
        #     print("⚠️ fallback reminder thread also failed:", e2)
    speak_text("Hello I am Aayu Mitra. How can I help you today?", lang="en")


    # Initialize conversation history (last 5 turns)
    conversation_history = deque(maxlen=5)

    # MAIN interactive loop
    while True:
        try:
            # cmd = input("\nPress [Enter] to speak or type 'q' to quit: ").strip()
            # if cmd.lower() == 'q':
            #     print("Exiting.")
            #     break

            # quick in-memory check (backwards compatibility)
            # try:
            #     reminder_message = None
            #     if 'check_reminders' in globals():
            #         reminder_message = check_reminders()
            #     if reminder_message:
            #         print("🔔 Local reminder:", reminder_message)
            #         speak_text(reminder_message)
            # except Exception:
            #     pass

            # Record
            # print("Recording for 6s... speak now.")
            record_voice(filename="input.wav", duration=10)

            # Transcribe (SpeechRecognition - uses selected language as hint)
            # lang_hint = select_language()
            text = transcribe_audio_sr("input.wav", language="hi")
            if not text:
                print("⚠️ No transcription. Try again.")
                continue

            print("📄 You said:", text)
            # local context log
            try:
                log_message("user", text)
            except Exception:
                pass

            # Firestore: log as message (sender Elderly)
            # try:
            #     firebase.add_message(PI_ID, "Elderly", text)
            # except Exception as e:
            #     print("⚠️ Failed to write message to Firestore:", e)

            # SOS detection
            if detect_sos(text):
                print("🚨 SOS detected!")
                try:
                    firebase.add_alert(PI_ID, "high", "assistant", f"SOS: {text}")
                except Exception as e:
                    print("⚠️ Failed to log alert to Firestore:", e)
                trigger_emergency_alert(text)

            # Detect language from text
            detected = detect_language(text)
            tts_lang = 'hi' if detected == 'hi' else 'en'

            # --- Gather Context from Firebase ---
            context_parts = []
            
            # 1. User Profile
            try:
                prof = firebase.get_user_profile(PI_ID)
                if not prof:
                    print("⚠️ Firebase profile missing. Using local demo profile.")
                    prof = DEMO_PROFILE
                else:
                    print("✅ Using User Profile from Firebase")

                if prof:
                    name = prof.get("name", "User")
                    age = prof.get("age", "?")
                    notes = prof.get("notes", "")
                    context_parts.append(f"User Profile: Name={name}, Age={age}, Notes={notes}")
                    
                    # Sleep Schedule from Profile
                    sleep = prof.get("sleep_schedule", {})
                    if sleep:
                        bed = sleep.get("planned_bedtime", "?")
                        wake = sleep.get("planned_wakeup", "?")
                        context_parts.append(f"Sleep Routine: Bedtime={bed}, Wakeup={wake}")
            except Exception as e:
                print(f"⚠️ Error fetching user profile: {e}. Using local demo profile.")
                # Fallback on error as well
                prof = DEMO_PROFILE
                name = prof.get("name", "User")
                context_parts.append(f"User Profile (Demo): Name={name}")

            # 2. Medications
            try:
                meds = firebase.get_medications(PI_ID)
                if meds:
                    med_list = [f"{m.get('title')} ({m.get('amount')}, {','.join(m.get('time_slots',[]))})" for m in meds]
                    context_parts.append("Medications: " + "; ".join(med_list))
            except:
                pass

            # 3. Daily Routines
            try:
                routines = firebase.get_routines(PI_ID)
                if routines:
                    rout_list = [f"{r.get('title')} at {r.get('time')} ({','.join(r.get('repeat_days',[]))})" for r in routines]
                    context_parts.append("Daily Routines: " + "; ".join(rout_list))
            except Exception as e:
                print("⚠️ Error fetching routines:", e)

            # 4. Upcoming Reminders
            try:
                upcoming = firebase.get_upcoming_reminders(PI_ID)
                if upcoming:
                    lines = []
                    for r in upcoming:
                        t = r.get("time", "??:??")
                        msg = r.get("message") or r.get("label") or "Reminder"
                        lines.append(f"- At {t}: {msg}")
                    context_parts.append("Upcoming Reminders: " + "; ".join(lines))
            except Exception as e:
                print("⚠️ Error fetching context reminders:", e)

            extra_context = "\n".join(context_parts)

            # LLM reply
            reply = get_emotional_reply(text, lang=detected, mode=LLM_MODE, history=list(conversation_history), extra_context=extra_context)
            
            # Update history
            conversation_history.append((text, reply))
            print(f"DEBUG: History updated. Current size: {len(conversation_history)}")
            print("🤖 Assistant:", reply)

            # log assistant reply locally
            try:
                log_message("assistant", reply)
            except Exception:
                pass

            # store assistant reply as message in Firestore
            try:
                firebase.add_message(PI_ID, text, reply)
            except Exception as e:
                print("⚠️ Failed to store assistant message in Firestore:", e)

            # speak reply
            try:
                speak_text(reply, lang=tts_lang)
            except Exception as e:
                print("❌ TTS playback error:", e)

        except KeyboardInterrupt:
            print("\nInterrupted. Exiting.")
            break
        except Exception as e:
            print("Unhandled error in main loop:", e)
            traceback.print_exc()
            # continue on error

if __name__ == "__main__":
    main()
