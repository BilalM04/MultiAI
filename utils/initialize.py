import streamlit as st
from langchain_community.tools import DuckDuckGoSearchRun, WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from utils.constants import default_text_model, default_tts_model, default_stt_model, default_search_tool, search_tool_options
from models.active_models import get_voices
from services.database import load_chats

def initialize():
    st.set_page_config(page_title="MultiAI", page_icon="./assets/robot.png")

    if "toast" in st.session_state:
        st.toast(st.session_state.toast["message"], icon=st.session_state.toast["icon"])
        del st.session_state.toast

    if 'chatbot_messages' not in st.session_state:
        st.session_state.chatbot_messages = []

    if 'search_messages' not in st.session_state:
        st.session_state.search_messages = []

    if "voice_messages" not in st.session_state:
        st.session_state.voice_messages = []

    if 'qna_messages' not in st.session_state:
        st.session_state.qna_messages = []

    if 'chat_histories' not in st.session_state:
        st.session_state.chat_histories = {}

    if "audio_input_key" not in st.session_state:
        st.session_state.audio_input_key = "audio_input_widget"

    if "upload_key" not in st.session_state:
        st.session_state.upload_key = "upload_widget"

    if "login_email_key" not in st.session_state:
        st.session_state.login_email_key = "login_email"

    if "login_password_key" not in st.session_state:
        st.session_state.login_password_key = "login_password"

    if "signup_email_key" not in st.session_state:
        st.session_state.signup_email_key = "signup_email"

    if "signup_password_key" not in st.session_state:
        st.session_state.signup_password_key = "signup_password"

    if 'duckduckgo_tool' not in st.session_state:
        st.session_state.duckduckgo_tool = DuckDuckGoSearchRun(name="Search")

    if 'wikipedia_tool' not in st.session_state:
        st.session_state.wikipedia_tool = WikipediaQueryRun(
            api_wrapper=WikipediaAPIWrapper()
        )

    if 'selected_text_model' not in st.session_state:
        st.session_state.selected_text_model = default_text_model

    if 'selected_tts_model' not in st.session_state:
        st.session_state.selected_tts_model = default_tts_model

    if 'selected_stt_model' not in st.session_state:
        st.session_state.selected_stt_model = default_stt_model

    if 'selected_tts_voice' not in st.session_state:
        st.session_state.selected_tts_voice = get_voices(st.session_state.selected_tts_model)[0]

    if 'selected_search_tool' not in st.session_state:
        st.session_state.selected_search_tool = default_search_tool

    if 'user' not in st.session_state:
        st.session_state.user = None

    if 'id_token' not in st.session_state:
        st.session_state.id_token = None

    if 'refresh_token' not in st.session_state:
        st.session_state.refresh_token = None

    if 'local_id' not in st.session_state:
        st.session_state.local_id = None

    if "load_chats" in st.session_state:
        load_chats()
        del st.session_state.load_chats
