import speech_recognition as sr

def transcribe_audio_sr(file_path="input.wav", language="hi-IN"):
    r = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        print("🎧 Listening...")
        audio = r.record(source)
    try:
        text = r.recognize_google(audio, language=language)
        return text
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError as e:
        return f"Google API Error: {str(e)}"
