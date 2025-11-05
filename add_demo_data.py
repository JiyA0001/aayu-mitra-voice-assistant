from utils.aayu_firebase import (
    set_user_profile, add_medication, add_routine,
    add_reminder, add_health_record, add_sleep_log,
    add_alert, add_message, init_db, PI_ID
)
from google.cloud import firestore
import datetime

init_db()  # ensure connection

# 1) user profile
set_user_profile(PI_ID, {
    "name": "Smt. Saraswati",
    "age": 74,
    "notes": "Hears well with hearing aid, prefers Hindi",
    "sleep_schedule": {"planned_bedtime": "22:00", "planned_wakeup": "06:00"}
})
print("User profile set")

# 2) medication
add_medication(PI_ID, {
    "pi_id": PI_ID, "title": "Paracetamol", "category": "Pill",
    "amount": "1 pill", "time_slots": ["Morning"], "repeat_days": ["Daily"]
})
print("Medication added")

# 3) routine
add_routine(PI_ID, {"pi_id": PI_ID, "title":"Morning Walk", "time":"06:30", "repeat_days":["Daily"], "notes":"Walk for 20 mins"})
print("Routine added")

# 4) reminder (one-off)
add_reminder(PI_ID, {"pi_id": PI_ID, "label":"Doctor", "details":"Clinic visit", "date":"2025-06-20", "time":"15:00", "priority":"High", "completed":False})
print("Reminder added")

# 5) health record
add_health_record(PI_ID, {
    "pi_id": PI_ID, "date": firestore.SERVER_TIMESTAMP,
    "weight_kg": 68.2, "blood_pressure": "130/80", "heart_rate_bpm": 76, "temperature_f": 98.4
})
print("Health record added")

# 6) sleep log
add_sleep_log(PI_ID, {"pi_id": PI_ID, "date":"2025-06-14", "duration_hours": 7.2})
print("Sleep log added")

# 7) alert
add_alert(PI_ID, "high", "Pipeline_A_LLM", "User reported dizziness and nausea.")
print("Alert added")

# 8) message
add_message(PI_ID, "Mitara", "Good morning! Time for your morning walk.")
print("Message added")
