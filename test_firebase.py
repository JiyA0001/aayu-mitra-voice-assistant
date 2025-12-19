from utils.aayu_firebase import init_db, _collection, PI_ID
import time

init_db()

docs = _collection("medication").where("pi_id", "==", PI_ID).stream()

for d in docs:
    print(d.id, d.to_dict())

try:
    # beep simulation for non-windows
    print("\a") 
    time.sleep(0.2)
except:
    print("nooo")