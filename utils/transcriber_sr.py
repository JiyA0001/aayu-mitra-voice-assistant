import speech_recognition as sr

recognizer = sr.Recognizer()
recognizer.dynamic_energy_threshold = False
recognizer.energy_threshold = 200

def transcribe_audio_sr(file_path="input.wav", language="hi-IN"):
    with sr.AudioFile(file_path) as source:
        print("🎧 Listening...")
        audio = recognizer.record(source)

    try:
        return recognizer.recognize_google(audio, language=language)
    except sr.UnknownValueError:
        return None
    except sr.RequestError as e:
        print("Speech API error:", e)
        return None
