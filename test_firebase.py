from utils.aayu_firebase import init_db, _collection, PI_ID
init_db()
docs = _collection("medication").where("pi_id", "==", PI_ID).stream()
for d in docs:
    print(d.id, d.to_dict())
