import whisper

model = whisper.load_model("base")  # or "small", "medium", "large"

def transcribe_audio_whisper(file_path="input.wav", language=None):
    """
    Transcribes audio using Whisper.
    :param file_path: Path to WAV file
    :param language: Force language (e.g., "hi" or "en")
    """
    print("🧠 Transcribing with Whisper...")
    result = model.transcribe(file_path, language=language)
    return result["text"].strip()


def detect_audio_language(file_path="input.wav"):
    model = whisper.load_model("base")
    audio = whisper.load_audio(file_path)
    audio = whisper.pad_or_trim(audio)
    mel = whisper.log_mel_spectrogram(audio).to(model.device)

    # Detect language
    _, probs = model.detect_language(mel)
    detected_lang = max(probs, key=probs.get)
    if probs[detected_lang] < 0.8:
        print("⚠️ Low confidence in language detection. Defaulting to 'en'")
        detected_lang = "en"
    print(f"🌐 Detected language: {detected_lang}")
    return detected_lang

def transcribe_audio_whisper_dynamic(file_path="input.wav"):
    lang = detect_audio_language(file_path)  # dynamically detect
    model = whisper.load_model("base")
    result = model.transcribe(file_path, language=lang, task="transcribe")
    return result["text"].strip(), lang
