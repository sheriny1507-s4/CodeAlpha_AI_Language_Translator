import streamlit as st
from datetime import datetime
from utils import translate_text, create_audio, languages
from deep_translator import GoogleTranslator
import speech_recognition as sr


# ===============================
# VOICE INPUT
# ===============================
def recognize_speech():


    recognizer = sr.Recognizer()

    try:

        with sr.Microphone() as source:

            st.info("🎤 Listening... Please speak.")

            recognizer.adjust_for_ambient_noise(source, duration=1)

            audio = recognizer.listen(source)

            text = recognizer.recognize_google(audio)

            st.success("✅ Voice captured successfully!")

            return text

    except sr.UnknownValueError:

        st.error("❌ Could not understand your voice.")

        return ""

    except sr.RequestError:

        st.error("❌ Speech recognition service unavailable.")

        return ""

    except Exception as e:

        st.error(f"❌ {e}")

        return ""
# ===============================
# PAGE CONFIG
# ===============================

st.set_page_config(
    page_title="🌍 AI Language Translation Tool",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ===============================
# LOAD CSS
# ===============================

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ===============================
# SESSION STATE
# ===============================

if "history" not in st.session_state:
    st.session_state.history = []

if "voice_text" not in st.session_state:
    st.session_state.voice_text = ""   

if "total_translations" not in st.session_state:
    st.session_state.total_translations = 0

st.markdown("""
<style>
.block-container{
    padding-top:1rem !important;
}
</style>
""", unsafe_allow_html=True)
# ===============================
# HERO SECTION
# ===============================
st.markdown("""
<div style="text-align:center;padding-top:5px;padding-bottom:15px;">

<h1 style="
font-size:56px;
font-weight:800;
letter-spacing:-2px;
line-height:1;
margin-bottom:8px;
font-family:'Manrope',sans-serif;
color:white;">

🌍 AI Language Translator

</h1>

<p style="
font-size:20px;
font-weight:400;
color:#CBD5E1;
margin-top:0px;">

Translate between multiple languages instantly using Artificial Intelligence

</p>

</div>
""", unsafe_allow_html=True)
# ===============================
# DASHBOARD
# ===============================
st.markdown(
    "<div style='margin-top:-20px'></div>",
    unsafe_allow_html=True
)

m1, m2, m3, m4 = st.columns(4)


m1.metric(
    "🌍 Languages",
    f"{len(languages)}+"
)

m2.metric(
    "🔄 Total Translations",
    st.session_state.total_translations
)

m4.metric(
    "🤖 AI",
    "Enabled"
)

st.markdown("<br>", unsafe_allow_html=True)

# ===============================
# INPUT SECTION
# ===============================

MAX_CHARS = 5000

left, right = st.columns([2, 1])

# ===============================
# LEFT CARD
# ===============================

with left:

    voice_col1, voice_col2 = st.columns([4, 1])

    with voice_col1:

        text = st.text_area(
            "✍ Enter Text",
            value=st.session_state.voice_text,
            placeholder="Type your text here...",
            height=220,
            key="input_text"
        )

    with voice_col2:

        st.write("")
        st.write("")

        voice = st.button(
            "🎤 Speak",
            use_container_width=True
        )

    st.progress(min(len(text) / MAX_CHARS, 1.0))

    st.caption(f"{len(text)} / {MAX_CHARS} Characters")


if voice:

    spoken_text = recognize_speech()

    if spoken_text:

        st.session_state.voice_text = spoken_text

        st.success("✅ Voice Captured Successfully!")

# Show what the user said
if st.session_state.voice_text:

    st.info(f"🎤 Spoken Text: {st.session_state.voice_text}")

# Refresh so the text box updates
if voice and spoken_text:

    st.rerun()
# ===============================
# RIGHT CARD
# ===============================

with right:

    source_language = st.selectbox(
        "🌍 Source Language",
        ["Auto Detect"] + list(languages.keys()),
        key="source_lang"
    )

    target_language = st.selectbox(
        "🌐 Target Language",
        list(languages.keys()),
        key="target_lang"
    )

    st.write("")
    translate = st.button(
    "🚀 Translate",
    use_container_width=True,
    key="translate_button"
    )
# ===============================
# TRANSLATE
# ===============================
# If voice input exists, use it
if st.session_state.voice_text.strip():
    text = st.session_state.voice_text

if translate:

    if text.strip() == "":

        st.warning("⚠ Please enter some text to translate.")

    else:

        try:

            with st.spinner("🌍 Translating..."):

                translated = translate_text(
                    text,
                    target_language,
                    languages
                )

            st.session_state.total_translations += 1

            

            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown('<div class="glass">', unsafe_allow_html=True)

            st.markdown("## 📄 Translated Text")
            st.caption("💡 Tip: Click inside the text box and press Ctrl + A, then Ctrl + C to copy the translation.")
            
            st.text_area(
                "Output",
                value=translated,
                height=180,
                key="output_text"
            )

            st.download_button(
                label="📥 Download Translation",
                data=translated,
                file_name="translated_text.txt",
                mime="text/plain",
                use_container_width=True
            )

            st.markdown("<br>", unsafe_allow_html=True)

            st.subheader("🔊 Listen")

            audio_file = create_audio(
                translated,
                languages[target_language]
            )

            with open(audio_file, "rb") as audio:

                st.audio(
                    audio.read(),
                    format="audio/mp3"
                )

            st.markdown("</div>", unsafe_allow_html=True)

            st.session_state.history.append({

                "time": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),

                "original": text,

                "translated": translated,

                "language": target_language

            })

            # Clear voice text after successful translation
            st.session_state.voice_text = ""

        except Exception as e:

            st.error(f"❌ {e}")
            # ===============================
# TRANSLATION HISTORY
# ===============================

if st.session_state.history:

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="glass">
    <h2>🕒 Translation History</h2>
    </div>
    """, unsafe_allow_html=True)

    for item in reversed(st.session_state.history):

        with st.expander(
            f"🌐 {item['language']} | 🕒 {item['time']}"
        ):

            st.markdown("### 📝 Original Text")

            st.write(item["original"])

            st.markdown("---")

            st.markdown("### 🌍 Translated Text")

            st.write(item["translated"])

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🗑 Clear History", use_container_width=True):

        st.session_state.history = []

        st.session_state.total_translations = 0

        st.rerun()

# ===============================
# FOOTER
# ===============================

st.markdown("""
<div class="footer">

<h2>🚀 Developed by Sherin Y</h2>

<p>
CodeAlpha Artificial Intelligence Internship
</p>
<hr style="
border:none;
height:1px;
background:rgba(255,255,255,0.25);
width:100%;
margin:30px auto;
">

<small>
AI Language Translation Tool • Powered by Streamlit • 2026
</small>

</div>
""", unsafe_allow_html=True)