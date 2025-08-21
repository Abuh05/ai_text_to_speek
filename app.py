import streamlit as st
import asyncio
import edge_tts
import tempfile

st.set_page_config(page_title="Edge TTS", page_icon="🔊", layout="centered")
st.title("🔊 Text-to-Speech (Edge-TTS)")
st.caption("Online TTS via Microsoft Edge voices (no PyTorch/NumPy).")

# A couple of sample voices; you can list many more from edge-tts docs
VOICES = [
    "en-US-AriaNeural",
    "en-US-GuyNeural",
    "en-GB-LibbyNeural",
    "en-AU-NatashaNeural",
]

text = st.text_area("Enter text:", "Hello! This uses Edge TTS.", height=140, key="edge_text")
voice = st.selectbox("Voice:", VOICES, index=0, key="edge_voice")
rate = st.slider("Rate (%)", -50, 50, 0, key="edge_rate")
pitch = st.slider("Pitch (semitones)", -10, 10, 0, key="edge_pitch")

async def synthesize(text, voice, rate, pitch):
    communicate = edge_tts.Communicate(
        text,
        voice=voice,
        rate=f"{rate:+d}%",
        pitch=f"{pitch:+d}Hz",
    )
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
        out_path = f.name
    await communicate.save(out_path)
    return out_path

if st.button("Generate Speech", key="edge_generate"):
    if not text.strip():
        st.warning("Please enter some text.")
    else:
        with st.spinner("Generating..."):
            audio_path = asyncio.run(synthesize(text, voice, rate, pitch))
        st.audio(audio_path, format="audio/mp3")
        with open(audio_path, "rb") as f:
            st.download_button("💾 Download MP3", f, file_name="tts_output.mp3", key="edge_download")
