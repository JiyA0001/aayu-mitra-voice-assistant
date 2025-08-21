from utils.voice_recorder import record_voice
from utils.transcriber_whisper import transcribe_audio_whisper, transcribe_audio_whisper_dynamic
from llm.emotion_model import get_emotional_reply
from config import LLM_MODE
from utils.text_to_speech import speak_text
from utils.transcriber_sr import transcribe_audio_sr
from utils.context_logger import log_message
from features.reminders import check_reminders, reminder_loop
from features.sos import detect_sos, trigger_emergency_alert
import threading


def detect_language(text: str) -> str:
    for char in text:
        if '\u0900' <= char <= '\u097F':
            return 'hi'  # Hindi
    return 'en'  # Default to English


def select_language():
    choice = input("🗣️ Speak in [1] Hindi or [2] English? (1/2): ")
    return "hi-IN" if choice.strip() == "1" else "en-IN"

def main():
    print("🎙️ Starting Elderly Voice Assistant (Speech → LLM)")
    cmd = input("\nPress [Enter] to speak or type 'q' to quit: ")
    # if cmd.lower() == 'q':
    #     break

    lang = select_language()
    # ✅ Step 0: Start the background reminder thread
    reminder_thread = threading.Thread(target=reminder_loop, daemon=True)
    reminder_thread.start()

    while True:
        reminder_message = check_reminders()
        if reminder_message:
            print("🔔 Reminder:", reminder_message)
            speak_text(reminder_message)
            

        # Step 1: Record audio
        record_voice(filename="input.wav", duration=6)

        # Step 2: Transcribe
        # text = transcribe_audio_whisper("input.wav", language=lang)  # auto-detect language
        text = transcribe_audio_sr("input.wav", language=lang)  # auto-detect language
        print(f"📄 You said: {text}")
        log_message("user", text)
        # text, lang = transcribe_audio_whisper_dynamic("input.wav")
        # print("📄 You said:", text)

        if detect_sos(text):
            trigger_emergency_alert(text)
        
        # Step 3: Detect language
        lang = detect_language(text)

        # Step 4: Get emotional reply
        reply = get_emotional_reply(text, lang=lang, mode=LLM_MODE)  # or "openai"
        print(f"🤖 Assistant: {reply}")
        log_message("assistant", reply)
        speak_text(reply, lang=lang)  # 'hi' or 'en'

if __name__ == "__main__":
    main()
