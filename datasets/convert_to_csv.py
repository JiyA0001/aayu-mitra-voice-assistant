import json
import pandas as pd

def jsonl_to_csv(jsonl_path, csv_path):
    data = []

    with open(jsonl_path, "r", encoding="utf-8") as f:
        for line in f:
            item = json.loads(line)
            hi_dialog = " ".join(item["dialog_hi"]).strip()
            emotion = item["emotion"].lower()
            data.append({"dialogue_hi": hi_dialog, "emotion": emotion})

    df = pd.DataFrame(data)
    
    # Optional: Filter only 6–8 major emotions if needed
    target_emotions = ['joy', 'sadness', 'anger', 'fear', 'neutral', 'surprise', 'love', 'disgust']
    df = df[df['emotion'].isin(target_emotions)]

    df.to_csv(csv_path, index=False, encoding="utf-8")
    print(f"✅ Saved to {csv_path} with {len(df)} entries")

if __name__ == "__main__":
    jsonl_to_csv("datasets/translated_dailydialog_hi.jsonl", "datasets/hindi_emotions.csv")
