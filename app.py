# app.py
import streamlit as st
import soundfile as sf
from kokoro import KPipeline
import torch
import io

# Load the Kokoro TTS Pipeline
@st.cache_resource
def load_pipeline():
    return KPipeline(lang_code="a")

pipeline = load_pipeline()

# Streamlit UI
st.set_page_config(page_title="Kokoro TTS App", page_icon="🎙️", layout="centered")

st.title("🎙️ Kokoro Text-to-Speech App")
st.markdown("Convert your text into **natural-sounding speech** using the Kokoro model.")

# Text Input
text = st.text_area("📝 Enter your text here:", height=150, placeholder="Type something to convert to speech...")

# Voice Selection
voices = ["af_heart", "af_sky", "af_glow", "af_hope"]
voice = st.selectbox("🎤 Choose a voice:", voices)

# Generate Button
if st.button("🔊 Generate Speech"):
    if text.strip() == "":
        st.warning("⚠️ Please enter some text.")
    else:
        st.info("🎶 Generating speech... Please wait.")
        generator = pipeline(text, voice=voice)

        for i, (gs, ps, audio) in enumerate(generator):
            # Convert to WAV bytes for playback and download
            wav_bytes = io.BytesIO()
            sf.write(wav_bytes, audio, 24000, format="WAV")
            wav_bytes.seek(0)

            st.audio(wav_bytes, format="audio/wav")
            st.download_button(
                label="💾 Download Audio",
                data=wav_bytes,
                file_name=f"tts_output_{i}.wav",
                mime="audio/wav"
            )
