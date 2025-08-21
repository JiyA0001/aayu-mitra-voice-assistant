# from gtts import gTTS
# import os

# def speak(text, lang='hi'):
#     tts = gTTS(text=text, lang=lang)
#     tts.save("output.mp3")
#     os.system("start output.mp3")  # Uses default player in Windows

# # Test
# speak("नमस्ते! आप कैसे हैं?", lang="hi")



# import json

# with open("data/emotion_samples_hi.jsonl", encoding='utf-8') as f:
#     for line in f:
#         obj = json.loads(line)
#         print("User:", obj["user"])
#         print("Assistant:", obj["assistant"])
#         print("---")


# from llm.emotion_model import build_prompt

# prompt = build_prompt("मुझे बहुत चिंता हो रही है।", lang="hi")
# print(prompt)
# speak(prompt, lang="hi")

# from utils.voice_recorder import record_voice

# record_voice(duration=4)  # Record for 4 seconds

# from utils.transcriber_whisper import transcribe_audio_whisper

# text = transcribe_audio_whisper("input.wav", language="hi")  # or "en"
# print("📄 Transcription:", text)

# from utils.transcriber_sr import transcribe_audio_sr

# text = transcribe_audio_sr("input.wav", language="hi-IN")
# print("📄 Transcription:", text)

# import os
# import google.generativeai as genai
# from dotenv import load_dotenv

# load_dotenv()
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
# models = genai.list_models()
# for m in models:
#     print(m.name, m.supported_generation_methods)

from llm.llm_gemini import get_gemini_reply
your_prompt="""ऐसे व्यवहार करें जैसे आप एक दयालु, हिंदी में बोलने वाले सहायक हैं। 
आपका काम बुज़ुर्ग उपयोगकर्ताओं को भावनात्मक सहारा देना है। 
आप हर उत्तर को केवल **सरल और शुद्ध हिंदी** में दें, बिना किसी अंग्रेज़ी शब्द के। 
उत्तर छोटे और सुकून देने वाले होने चाहिए। एक ही वाक्य में उत्तर दें।
"""
r=get_gemini_reply("मैं बहुत अकेली हूँ", system_prompt=your_prompt)
print(r)