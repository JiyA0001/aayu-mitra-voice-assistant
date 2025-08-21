from datasets import load_dataset
from googletrans import Translator
from transformers import pipeline
import json

def translate_and_label():
    # Load dataset with trust for remote code
    dataset = load_dataset("daily_dialog", trust_remote_code=True)
    samples = []

    # Limit to 100 short conversations
    for item in dataset['train']:
        if len(item['dialog']) <= 2:
            samples.append(item)
        if len(samples) >= 100:
            break

    # Setup translator & emotion classifier
    translator = Translator()
    emotion_classifier = pipeline("text-classification", model="bhadresh-savani/distilbert-base-uncased-emotion")

    # Process each dialogue
    processed = []
    for conv in samples:
        dialog_en = conv["dialog"]
        dialog_hi = [translator.translate(utt, src='en', dest='hi').text for utt in dialog_en]

        # Join last 2 utterances for emotion detection
        context = " ".join(dialog_en[-2:])
        prediction = emotion_classifier(context)[0]["label"]

        processed.append({
            "dialog_en": dialog_en,
            "dialog_hi": dialog_hi,
            "emotion": prediction.lower()
        })

    # Save to JSONL
    with open("datasets/translated_dailydialog_hi.jsonl", "w", encoding='utf-8') as f:
        for item in processed:
            json.dump(item, f, ensure_ascii=False)
            f.write("\n")

if __name__ == "__main__":
    translate_and_label()
