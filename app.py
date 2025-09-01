import streamlit as st
import asyncio
import edge_tts
import tempfile

# ---------- Page Config ----------
st.set_page_config(
    page_title="Edge TTS",
    page_icon="🔊",
    layout="centered"
)

# ---------- Header ----------
st.markdown(
    """
    <h1 style='text-align: center; color: #4CAF50;'>🔊 Edge Text-to-Speech</h1>
    <p style='text-align: center; color: gray;'>
        Generate natural-sounding speech using Microsoft Edge voices 🎙️
    </p>
    <hr style="margin-top:10px;margin-bottom:20px;">
    """,
    unsafe_allow_html=True
)

# ---------- Voice Options ----------
VOICES = [
    "en-US-AriaNeural",
    "en-US-GuyNeural",
    "en-GB-LibbyNeural",
    "en-AU-NatashaNeural",
]

# ---------- Sidebar Controls ----------
st.sidebar.header("⚙️ Settings")
voice = st.sidebar.selectbox("🎤 Voice", VOICES, index=0, key="edge_voice")
rate = st.sidebar.slider("⏩ Rate (%)", -50, 50, 0, key="edge_rate")
pitch = st.sidebar.slider("🎵 Pitch (semitones)", -10, 10, 0, key="edge_pitch")

# ---------- Text Input ----------
st.subheader("📝 Enter your text")
text = st.text_area(
    "Your text will be converted into speech:",
    "Hello! This uses Edge TTS.",
    height=140,
    key="edge_text"
)

# ---------- TTS Function ----------
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

# ---------- Action Button ----------
st.markdown("### 🚀 Generate Speech")
if st.button("🎧 Generate & Listen", key="edge_generate", use_container_width=True):
    if not text.strip():
        st.warning("⚠️ Please enter some text before generating.")
    else:
        with st.spinner("🎙️ Generating speech..."):
            audio_path = asyncio.run(synthesize(text, voice, rate, pitch))
        st.success("✅ Speech generated successfully!")
        st.audio(audio_path, format="audio/mp3")
        with open(audio_path, "rb") as f:
            st.download_button(
                "💾 Download MP3",
                f,
                file_name="tts_output.mp3",
                key="edge_download",
                use_container_width=True
            )

# ---------- Footer ----------
st.markdown(
    """
    <hr>
    <p style='text-align: center; color: gray; font-size: 0.9em;'>
        Built with ❤️ using <b>Streamlit</b> & <b>Edge TTS</b>
    </p>
    """,
    unsafe_allow_html=True
)
