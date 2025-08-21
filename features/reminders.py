# reminder_db = {}  # {user_id: [("Take medicine", "8 PM")]}

# def set_reminder(user_id, message, time):
#     if user_id not in reminder_db:
#         reminder_db[user_id] = []
#     reminder_db[user_id].append((message, time))

# def get_reminders(user_id):
#     return reminder_db.get(user_id, [])


# features/reminders.py

# features/reminders.py

import datetime
import time
import threading
from utils.text_to_speech import speak_text  # assuming this uses gTTS and plays audio

# 📝 Simulated reminders (will be replaced by DB in Phase 3)
reminders = [
    {"time": "15:37", "message": "दवाई खा लीजिए।"},
    {"time": "15:40", "message": "सोने का समय हो गया है।"},
]

def check_reminders():
    now = datetime.datetime.now().strftime("%H:%M")
    for reminder in reminders:
        if reminder["time"] == now:
            return reminder["message"]
    return None

def reminder_loop():
    print("🔁 Reminder loop started in background...")
    last_triggered = set()
    while True:
        reminder = check_reminders()
        if reminder and reminder not in last_triggered:
            print("🔔 Reminder:", reminder)
            speak_text(reminder)
            last_triggered.add(reminder)
        time.sleep(60)  # Check every 60 seconds
