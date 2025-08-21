# 👵 Elderly Emotional Support Voice Assistant

A beginner-friendly, voice-based AI assistant designed to provide emotional support to elderly users using speech recognition, local or cloud-based LLMs, and text-to-speech synthesis — all integrated in a lightweight, privacy-conscious setup.

---

## 📌 Features

- 🎤 **Speech-to-Text** using Google API or Whisper (Hindi + English)
- 🤖 **LLM Integration** (TinyLLama, Gemma, Phi or GPT-3.5 via API)
- 💬 **Emotionally sensitive replies** tailored for elderly users
- 🔊 **Voice output** using `gTTS` in Hindi or English
- 🌐 Configurable local/cloud support for offline or production use

---

## 🛠️ Tech Stack

- Python 3.11+
- gTTS & pygame (TTS)
- SpeechRecognition / Whisper (STT)
- Ollama (for local LLMs like Gemma)
- OpenAI API (optional)
- sounddevice / scipy (audio handling)

---

## 🚀 How to Run

```bash
git clone https://github.com/JiyA0001/voice-assistant.git
cd voice-assistant
python -m venv .venv
.\.venv\Scripts\activate

pip install -r requirements.txt

# Run the assistant
python main_voice_loop.py
```

### 🔔 Reminders

- Simulates a working reminder system using a hardcoded list.
- At every run, the system checks if any reminder matches the current time.
- If a match is found, the assistant vocalizes it in Hindi using gTTS.
- Future versions will connect to a database for persistent reminders.

### 🔔 Real-Time Background Reminders
- The assistant starts a background thread that checks for demo reminders every minute.
- This runs independently of the user interaction loop.
- In Phase 3, it will query reminders from a real-time database.

### 🧠 Dataset Preparation

To prepare translated and labeled DailyDialog samples:

```bash
cd datasets
python dailydialog_translator.py
```

### Fine-Tuning Ready Datasets

- `hindi_emotions_clean.csv`: Cleaned dialogue-emotion pairs (text, label)
- `hindi_emotions_clean.jsonl`: JSONL format, compatible with LLM fine-tuning (Hugging Face, OpenAI fine-tune APIs, etc.)
