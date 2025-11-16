import streamlit as st
from models.active_models import text_models, tts_models, stt_models, get_voices
from utils.constants import search_tool_options, chatbot_state, searchbot_state, voicebot_state, fileqna_state, about_state
import time

def clear_chat_history(state):
    if state == chatbot_state:
        st.session_state.chatbot_messages = []
    elif state == searchbot_state:
        st.session_state.search_messages = []
    elif state == voicebot_state:
        st.session_state.voice_messages = []
        st.session_state.audio_input_key = f"audio_input_widget_{time.time()}"
    elif state == fileqna_state:
        st.session_state.qna_messages = []

def render_sidebar(state):
    if state == fileqna_state:
        st.caption("⚠️ Navigating away from this tab will reset the chat.")
    
    if state == voicebot_state:
        selected_tts_model = st.selectbox("Text-to-Speech LLM", tts_models, index=tts_models.index(st.session_state.selected_tts_model))
        selected_tts_voice = st.selectbox("Text-to-Speech Voice", get_voices(selected_tts_model), index=get_voices(selected_tts_model).index(st.session_state.selected_tts_voice))
        selected_stt_model = st.selectbox("Speech-to-Text LLM", stt_models, index=stt_models.index(st.session_state.selected_stt_model))
  
        if selected_stt_model != st.session_state.selected_stt_model:
            st.session_state.selected_stt_model = selected_stt_model

        if selected_tts_model != st.session_state.selected_tts_model:
            st.session_state.selected_tts_model = selected_tts_model

    if state != about_state:
        selected_text_model = st.selectbox("Response LLM", text_models, index=text_models.index(st.session_state.selected_text_model))

        if selected_text_model != st.session_state.selected_text_model:
            st.session_state.selected_text_model = selected_text_model

    if state == searchbot_state:
        selected_search_tool = st.selectbox("Search Tool", search_tool_options, index=search_tool_options.index(st.session_state.selected_search_tool))

        if selected_search_tool != st.session_state.selected_search_tool:
            st.session_state.selected_search_tool = selected_search_tool
    
    # Add custom CSS to style the button
    st.markdown("""
        <style>
        .full-width-button .stButton button {
            width: 100%;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Add the button with the custom CSS class
    if state != about_state:
        st.button(
            "Clear History", 
            key="clear_chat",
            help="Clear the chat history",
            on_click=lambda: clear_chat_history(state),
            args=(),
            kwargs={},
            disabled=False,
            use_container_width=True
        )
