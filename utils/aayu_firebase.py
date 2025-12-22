# utils/aayu_firebase.py
import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore

load_dotenv()

FIREBASE_CRED = os.getenv("FIREBASE_CRED", "aayumitra-f4141-d2d7f314cc6d.json")
APP_ID = os.getenv("APP_ID", "aayu-mitra")   # update to your app id
PI_ID = os.getenv("PI_ID", "pi-hub-001")     # the Pi's unique id

# Root base path as per contract: artifacts/{appId}/public/data
DATA_ROOT = f"artifacts/{APP_ID}/public/data"

_app = None
_db = None

def init_db():
    global _app, _db
    if _app is None:
        cred_path = os.path.abspath(FIREBASE_CRED)
        if not os.path.exists(cred_path):
            raise FileNotFoundError(f"Firebase credential not found: {cred_path}")
        cred = credentials.Certificate(cred_path)
        _app = firebase_admin.initialize_app(cred)
        _db = firestore.client()
    return _db

def _collection(name):
    """Return a CollectionReference for DATA_ROOT/{name}"""
    db = init_db()
    return db.collection(f"{DATA_ROOT}/{name}")

# ------------------ user_profile ------------------
def set_user_profile(pi_id: str, payload: dict):
    """
    payload example:
    {
      "name": "Elderly User Name",
      "age": 72,
      "notes": "Prefers Hindi",
      "sleep_schedule": {"planned_bedtime": "22:00", "planned_wakeup": "06:30"}
    }
    """
    col = _collection("user_profile")
    # document id is pi_id
    col.document(pi_id).set(payload, merge=True)

def get_user_profile(pi_id: str):
    doc = _collection("user_profile").document(pi_id).get()
    return doc.to_dict() if doc.exists else None

# ------------------ medication ------------------
def add_medication(pi_id: str, medication_payload: dict):
    """
    medication_payload example:
    {
      "pi_id": pi_id,
      "title": "Paracetamol",
      "category": "Pill",
      "amount": "2 pills",
      "time_slots": ["Morning","Night"],
      "repeat_days": ["Daily"]
    }
    """
    col = _collection("medication")
    return col.add(medication_payload)  # returns (ref, write_time)

def get_medications(pi_id: str):
    col = _collection("medication")
    docs = col.where("pi_id", "==", pi_id).stream()
    return [d.to_dict() for d in docs]

# ------------------ routines ------------------
def add_routine(pi_id: str, routine_payload: dict):
    """
    routine_payload example:
    {
      "pi_id": pi_id,
      "title": "Morning Walk",
      "time": "06:00",
      "repeat_days": ["Mon","Wed","Fri"],
      "notes": "Walk 20 minutes"
    }
    """
    col = _collection("routines")
    return col.add(routine_payload)

def get_routines(pi_id: str):
    col = _collection("routines")
    docs = col.where("pi_id", "==", pi_id).stream()
    return [d.to_dict() for d in docs]

# ------------------ reminders ------------------
def add_reminder(pi_id: str, reminder_payload: dict):
    """
    reminder_payload example:
    {
      "pi_id": pi_id,
      "label": "Doctor's Appointment",
      "details": "Annual checkup",
      "date": "2025-06-15",    # YYYY-MM-DD
      "time": "15:30",         # HH:MM
      "priority": "Normal",
      "completed": False
    }
    """
    col = _collection("reminders")
    return col.add(reminder_payload)

def get_due_reminders(pi_id: str, time_hhmm: str):
    """
    Query reminders in Firestore for this device where time == time_hhmm and not completed.
    Returns list of dicts with 'id' + fields.
    """
    col = _collection("reminders")
    # Query: pi_id == pi_id AND time == time_hhmm AND completed == False
    query = col.where("pi_id", "==", pi_id).where("time", "==", time_hhmm).where("completed", "==", False)
    docs = query.stream()
    out = []
    for d in docs:
        data = d.to_dict()
        data["id"] = d.id
        out.append(data)
    return out

def mark_reminder_completed(pi_id: str, reminder_id: str):
    col = _collection("reminders")
    doc_ref = col.document(reminder_id)
    doc_ref.update({"completed": True, "completed_at": firestore.SERVER_TIMESTAMP})

def get_upcoming_reminders(pi_id: str):
    """
    Fetch all incomplete reminders for the user.
    """
    col = _collection("reminders")
    query = col.where("pi_id", "==", pi_id).where("completed", "==", False)
    docs = query.stream()
    out = []
    for d in docs:
        data = d.to_dict()
        data["id"] = d.id
        out.append(data)
    return out

# ------------------ health_records ------------------
def add_health_record(pi_id: str, record_payload: dict):
    """
    record_payload example:
    {
      "pi_id": pi_id,
      "date": firestore.SERVER_TIMESTAMP,  # or datetime
      "weight_kg": 68.5,
      "blood_pressure": "120/80",
      "heart_rate_bpm": 72,
      "temperature_f": 98.6
    }
    """
    col = _collection("health_records")
    return col.add(record_payload)

# ------------------ sleep_logs ------------------
def add_sleep_log(pi_id: str, sleep_payload: dict):
    """
    sleep_payload example:
    {
      "pi_id": pi_id,
      "date": "2025-06-14",
      "duration_hours": 7.5
    }
    """
    col = _collection("sleep_logs")
    return col.add(sleep_payload)

# ------------------ alerts ------------------
def add_alert(pi_id: str, level: str, source: str, message: str):
    """
    alert example structure:
    {
      "pi_id": pi_id,
      "level": "high" or "info",
      "source": "Pipeline_A_LLM",
      "message": "...",
      "timestamp": firestore.SERVER_TIMESTAMP,
      "acknowledged": False
    }
    """
    col = _collection("alerts")
    payload = {
        "pi_id": pi_id,
        "level": level,
        "source": source,
        "message": message,
        "timestamp": firestore.SERVER_TIMESTAMP,
        "acknowledged": False
    }
    return col.add(payload)

# ------------------ messages ------------------
def add_message(pi_id: str, user_input: str, output: str):
    """ 
    input: user input
    output: LLM response
    """
    col = _collection("messages")
    payload = {
        "pi_id": pi_id,
        "user_input": user_input,
        "output": output,
        "timestamp": firestore.SERVER_TIMESTAMP
    }
    return col.add(payload)

# ------------------ convenience example ------------------
if __name__ == "__main__":
    # quick smoke test (will run if module executed directly)
    init_db()
    print("Firestore initialized for", DATA_ROOT)
