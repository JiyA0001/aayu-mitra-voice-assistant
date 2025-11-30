from utils.aayu_firebase import init_db, _collection, PI_ID
import winsound
init_db()
docs = _collection("medication").where("pi_id", "==", PI_ID).stream()
for d in docs:
    print(d.id, d.to_dict())
try:
    winsound.Beep(1000, 200)   # frequency=1000 Hz, duration=200 ms
except:
    print("nooo")