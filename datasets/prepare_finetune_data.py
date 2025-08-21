import pandas as pd
import json

def prepare_data(input_csv, out_csv, out_jsonl):
    df = pd.read_csv(input_csv)

    # Optional: drop duplicates/nulls
    df = df.dropna().drop_duplicates()

    # Rename for clarity
    df = df.rename(columns={"dialogue_hi": "text", "emotion": "label"})

    # Save cleaned CSV
    df.to_csv(out_csv, index=False, encoding="utf-8")
    print(f"✅ Saved cleaned CSV: {out_csv}")

    # Save as JSONL (line-delimited)
    with open(out_jsonl, "w", encoding="utf-8") as f:
        for _, row in df.iterrows():
            record = {"text": row["text"], "label": row["label"]}
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"✅ Saved fine-tune JSONL: {out_jsonl}")

if __name__ == "__main__":
    prepare_data(
        input_csv="datasets/hindi_emotions.csv",
        out_csv="datasets/hindi_emotions_clean.csv",
        out_jsonl="datasets/hindi_emotions_clean.jsonl"
    )
