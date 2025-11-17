import streamlit as st
from models.active_models import text_models, tts_models, stt_models, get_voices
from utils.constants import search_tool_options, chatbot_state, searchbot_state, voicebot_state, fileqna_state, about_state, account_state
from services.database import save_chat
import time
import copy

# ---------------------------------------
# Clear Chat History
# ---------------------------------------
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

# ---------------------------------------
# Save Chat History Dialog
# ---------------------------------------
@st.dialog("Save Chat History")
def save_chat_dialog(history):
    st.write("Give your chat a name and press **Save** to store it permanently.")

    chat_name = st.text_input("📝 Chat Name", key="chat_name_input")

    if (chat_name in st.session_state.chat_histories):
        st.warning(f"A chat with this name already exists. Saving will overwrite the existing one.", icon=":material/warning:")

    # Save button
    if st.button("Save", key="save_chat_button", use_container_width=True):
        if not chat_name.strip():
            st.toast("Chat name cannot be empty.", icon=":material/warning:")
        else:
            save_chat(chat_name, history)
            st.rerun()

    st.divider()

    # History preview
    with st.expander("📃 Preview Current Conversation", expanded=False):
        st.caption("This is what will be saved:")

        for msg in history:
            st.chat_message(msg["role"]).markdown(msg["content"])

# ---------------------------------------
# Load Chat History Dialog
# ---------------------------------------
@st.dialog("Load Chat History")
def load_chat(state):
    st.write("Select a saved chat and press **Load** to replace the current conversation.")
    st.warning(f"The current conversation will be lost if it is not saved.", icon=":material/warning:")

    chat_names = list(st.session_state.chat_histories.keys())
    selected_chat = st.selectbox("📁 Saved Conversations", chat_names)
    chat_history = copy.deepcopy(st.session_state.chat_histories[selected_chat])

    # Save button
    if st.button("Load", key="load_chat_button", use_container_width=True):
        if state == chatbot_state:
            st.session_state.chatbot_messages = chat_history
        elif state == searchbot_state:
            st.session_state.search_messages = chat_history
        elif state == voicebot_state:
            st.session_state.voice_messages = chat_history
        
        st.session_state.toast = {
            "message": f"Successfully loaded chat '{selected_chat}'",
            "icon": ":material/check:"
        }
        st.rerun()

    st.divider()

    # History preview
    with st.expander("📃 Preview Selected Conversation", expanded=False):
        st.caption("This is what will be loaded:")

        for msg in chat_history:
            st.chat_message(msg["role"]).markdown(msg["content"])

# ---------------------------------------
# Log Out Dialog
# ---------------------------------------
@st.dialog("Log Out")
def log_out():
    st.write(f"Are you sure you want to log out of the account {st.session_state.user}?")

    if st.button("Log Out", key="log_out_button", use_container_width=True):
        st.session_state.user = None
        st.session_state.id_token = None
        st.session_state.refresh_token = None
        st.session_state.local_id = None
        st.session_state.chat_histories = []
        st.session_state.toast = {
            "message": "Successfully logged out of account",
            "icon": ":material/check:"
        }
        st.rerun()

# ---------------------------------------
# Render Sidebar
# ---------------------------------------
def render_sidebar(state):
    if state == fileqna_state:
        st.caption("⚠️ Navigating away from this tab will reset the chat.")

    is_user_logged_in = not any(st.session_state[key] is None for key in ("user", "id_token", "refresh_token", "local_id"))
    
    # Voicebot selections
    if state == voicebot_state:
        selected_tts_model = st.selectbox("Text-to-Speech LLM", tts_models, index=tts_models.index(st.session_state.selected_tts_model))
        selected_tts_voice = st.selectbox("Text-to-Speech Voice", get_voices(selected_tts_model), index=get_voices(selected_tts_model).index(st.session_state.selected_tts_voice))
        selected_stt_model = st.selectbox("Speech-to-Text LLM", stt_models, index=stt_models.index(st.session_state.selected_stt_model))
  
        if selected_stt_model != st.session_state.selected_stt_model:
            st.session_state.selected_stt_model = selected_stt_model

        if selected_tts_model != st.session_state.selected_tts_model:
            st.session_state.selected_tts_model = selected_tts_model

    # Chatbot, Searchbot, voicebot, and file q&a selection
    if state not in [about_state, account_state]:
        selected_text_model = st.selectbox("Response LLM", text_models, index=text_models.index(st.session_state.selected_text_model))

        if selected_text_model != st.session_state.selected_text_model:
            st.session_state.selected_text_model = selected_text_model

    # Searchbot tool selection
    if state == searchbot_state:
        selected_search_tool = st.selectbox("Search Tool", search_tool_options, index=search_tool_options.index(st.session_state.selected_search_tool))

        if selected_search_tool != st.session_state.selected_search_tool:
            st.session_state.selected_search_tool = selected_search_tool

    # Account logout button
    if state == account_state and is_user_logged_in:
        if st.button("Log Out", key="log_out", use_container_width=True):
            log_out()
     
    # Chat history buttons
    if state not in [about_state, account_state]:
        st.divider()

        if st.button("Clear Chat", key="clear_chat", use_container_width=True):
            clear_chat_history(state)
            st.toast("Cleared chat history", icon=":material/mop:")

        if state in [chatbot_state, searchbot_state, voicebot_state] and is_user_logged_in:
            history = []

            if state == chatbot_state:
                history = st.session_state.chatbot_messages
            elif state == searchbot_state:
                history = st.session_state.search_messages
            elif state == voicebot_state:
                history = st.session_state.voice_messages

            if st.button("Save Chat", key="save_chat",use_container_width=True):
                if history != []:
                    save_chat_dialog(history)
                else:
                    st.toast("Current chat conversation is empty", icon=":material/warning:")

            if st.button("Load Chat", key="load_chat",use_container_width=True):
                if st.session_state.chat_histories:
                    load_chat(state)
                else:
                    st.toast("No saved chats available", icon=":material/warning:")
