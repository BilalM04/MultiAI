import streamlit as st
from groq import Groq, RateLimitError
from utils.sidebar import render_sidebar
from utils.initialize import initialize
from utils.constants import rate_limit_message, generic_error_message, voicebot_state
from models.active_models import get_owner
import tempfile
import base64
import os
import time

# ---------------------------------------
# Initialize session
# ---------------------------------------
initialize()

# ---------------------------------------
# Groq Client
# ---------------------------------------
client = Groq(api_key=st.secrets.get("groq_api_key"))

# ---------------------------------------
# Sidebar
# ---------------------------------------
with st.sidebar:
    render_sidebar(voicebot_state)

# ---------------------------------------
# Page Header
# ---------------------------------------
st.title("🎙️ Voicebot")
st.caption(
    f"🚀 Chatbot powered by {st.session_state.selected_stt_model} ({get_owner(st.session_state.selected_stt_model)}), "
    f"{st.session_state.selected_text_model} ({get_owner(st.session_state.selected_text_model)}), and "
    f"{st.session_state.selected_tts_model} ({get_owner(st.session_state.selected_tts_model)})"
)

# ---------------------------------------
# Reset widgets when tab changes
# ---------------------------------------
def reset_audio_widgets():
    st.session_state.audio_input_key = f"audio_input_{time.time()}"
    st.session_state.upload_key = f"audio_upload_{time.time()}"
    st.session_state.audio_value = None

audio_value = None

# ---------------------------------------
# Tabs
# ---------------------------------------
record_tab = "🎙️ Record"
upload_tab = "📁 Upload"
history_tab = "📝 History"

tab = st.segmented_control(
    "Mode (switching tabs resets the current recording)",
    options=[record_tab, upload_tab, history_tab],
    default=record_tab,
    width="stretch",
    on_change=reset_audio_widgets
)

# ---------------------------------------
# RECORD TAB
# ---------------------------------------
if tab == record_tab:
    audio_value = st.audio_input(
        "Record high quality audio",
        sample_rate=48000,
        key=st.session_state.audio_input_key,
    )

# ---------------------------------------
# UPLOAD TAB
# ---------------------------------------
elif tab == upload_tab:
    uploaded_file = st.file_uploader(
        "Upload a WAV, MP3, or M4A file",
        type=["wav", "mp3", "m4a"],
        key=st.session_state.upload_key,
    )

    if uploaded_file:
        audio_value = uploaded_file
        st.audio(uploaded_file, format="audio/wav")

# ---------------------------------------
# HISTORY TAB
# ---------------------------------------
elif tab == history_tab:
    if not st.session_state.voice_messages:
        st.info("No conversation history yet.", icon="💬")
    else:
        for msg in st.session_state.voice_messages:
            st.chat_message(msg["role"]).markdown(msg["content"])

    st.stop()

# ---------------------------------------
# Record or Upload: No audio yet
# ---------------------------------------
if not audio_value:
    if (tab == record_tab):
        st.info("Record audio to start!", icon="🎙️")
    if (tab == upload_tab):
        st.info("Upload audio to start!", icon="🎧")
    st.stop()

# ---------------------------------------
# Save audio to WAV file
# ---------------------------------------
with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
    tmp_file.write(audio_value.getvalue())
    audio_path = tmp_file.name

# ---------------------------------------
# Speech to Text
# ---------------------------------------
with st.spinner("🧠 Transcribing the recording..."):
    time.sleep(0.5)
    try:
        transcription = client.audio.transcriptions.create(
            file=open(audio_path, "rb"),
            model=st.session_state.selected_stt_model
        )
    except RateLimitError:
        st.warning(rate_limit_message.format(model=st.session_state.selected_stt_model), icon=":material/warning:")
        st.stop()

user_text = transcription.text.strip()
user_message = { "role": "user", "content": user_text }

with st.expander(f"📜 Transcription complete using **{st.session_state.selected_stt_model}**", expanded=True):
    st.write(user_text)

# ---------------------------------------
# LLM RESPONSE
# ---------------------------------------
with st.spinner("💬 Generating AI response..."):
    try:
        chat = client.chat.completions.create(
            messages=st.session_state.voice_messages + [user_message],
            model=st.session_state.selected_text_model,
        )
    except RateLimitError:
        st.warning(rate_limit_message.format(model=st.session_state.selected_text_model), icon=":material/warning:")
        st.stop()

response = chat.choices[0].message.content.strip()
st.session_state.voice_messages.append(user_message)
st.session_state.voice_messages.append({ "role": "assistant", "content": response })

with st.expander(f"💬 Response generated using **{st.session_state.selected_text_model}**", expanded=True):
    st.write(response)

# ---------------------------------------
# Text-to-speech
# ---------------------------------------
with st.spinner("🔊 Generating AI voice response..."):
    try:
        tts_response = client.audio.speech.create(
            model=st.session_state.selected_tts_model,
            voice=st.session_state.selected_tts_voice,
            input=response,
            response_format="wav"
        )
    except RateLimitError:
        st.warning(rate_limit_message.format(model=st.session_state.selected_tts_model), icon=":material/warning:")
        st.stop()

with st.expander(f"🔊 Text-to-speech complete using **{st.session_state.selected_tts_model}** with voice **{st.session_state.selected_tts_voice}**", expanded=True):
    st.audio(tts_response.read(), format="audio/wav")
