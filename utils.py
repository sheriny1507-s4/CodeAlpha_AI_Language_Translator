from deep_translator import GoogleTranslator
from gtts import gTTS
import os

# ===============================
# TRANSLATE TEXT
# ===============================

def translate_text(text, target_language, languages):

    translated = GoogleTranslator(
        source="auto",
        target=languages[target_language]
    ).translate(text)

    return translated


# ===============================
# CREATE AUDIO
# ===============================

def create_audio(text, language_code):

    os.makedirs("audio", exist_ok=True)

    audio_path = "audio/output.mp3"

    tts = gTTS(
        text=text,
        lang=language_code,
        slow=False
    )

    tts.save(audio_path)

    return audio_path


# ===============================
# LANGUAGE LIST
# ===============================

languages = {

    "English":"en",
    "Hindi":"hi",
    "Kannada":"kn",
    "Tamil":"ta",
    "Telugu":"te",
    "Malayalam":"ml",
    "Marathi":"mr",
    "Gujarati":"gu",
    "Punjabi":"pa",
    "Urdu":"ur",
    "French":"fr",
    "German":"de",
    "Spanish":"es",
    "Italian":"it",
    "Portuguese":"pt",
    "Russian":"ru",
    "Japanese":"ja",
    "Korean":"ko",
    "Chinese":"zh-CN",
    "Arabic":"ar"
}