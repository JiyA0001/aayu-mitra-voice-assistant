def detect_language(text):
    if any(ord(c) > 128 for c in text):  # crude Hindi detection
        return "hi"
    return "en"
