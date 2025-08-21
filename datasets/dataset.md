# 📊 Datasets Overview

This folder will contain all datasets used for model fine-tuning, prompt engineering, and testing features.

---

## 1. Emotional Support – Hindi/English Prompts
- **File**: `emotion_samples_hi.jsonl`, `emotion_samples_en.jsonl`
- **Use**: Few-shot examples for emotional support replies in both languages
- **Fields**:
  - `user_input`: Input sentence
  - `assistant_reply`: Ideal response

---

## 2. Reminder Patterns Dataset
- **File**: `reminder_samples.jsonl`
- **Use**: Fine-tune or test time/date extraction (e.g., “कल रात 8 बजे मुझे दवा लेनी है”)

---

## 3. SOS Commands Dataset
- **File**: `sos_commands.json`
- **Use**: Keywords and phrases that trigger emergency support

---

## 4. Transcription & STT Test Clips
- **Folder**: `datasets/audio_samples/`
- **Files**: WAV/MP3 audio clips in Hindi and English for STT model testing

---

## 5. User Interaction Logs (For context training)
- **File**: `context_log_samples.jsonl`
- **Use**: Example session logs for context-aware generation

---

## 6. Future (Optional)
- Depression detection labeled dataset (e.g., DAIC-WOZ)
- Multimodal: Text + Audio emotion corpora (e.g., EMO-DB, CREMA-D)


### DailyDialog Hindi Emotion Dataset
- Translated 100 DailyDialog conversations to Hindi
- Auto-labeled emotions using HuggingFace transformer
- File: `translated_dailydialog_hi.jsonl`


### Hindi Emotions CSV
- File: `hindi_emotions.csv`
- Format: [Hindi dialogue, emotion]
- Label set: joy, sadness, fear, anger, neutral, surprise, love, disgust
- Extracted from translated DailyDialog dataset
