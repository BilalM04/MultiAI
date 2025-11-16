import streamlit as st
import time
from groq import Groq, RateLimitError
from utils.sidebar import render_sidebar
from utils.initialize import initialize
from models.active_models import get_owner

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
    render_sidebar(0)

# ---------------------------------------
# Page Header
# ---------------------------------------
st.title('💬 Chatbot')
st.caption("🚀 Chatbot powered by " + st.session_state.selected_text_model + " (" + get_owner(st.session_state.selected_text_model) + ")")

# ---------------------------------------
# Chat History
# ---------------------------------------
for message in st.session_state.chatbot_messages:
    st.chat_message(message['role']).markdown(message['content'])

# ---------------------------------------
# Prompt Input
# ---------------------------------------
prompt = st.chat_input('Pass your prompt here (max 500 characters)')

# ---------------------------------------
# LLM Response
# ---------------------------------------
if prompt and len(prompt) <= 500:
    st.chat_message('user').markdown(prompt)
    user_message = { 'role': 'user', 'content': prompt }
    
    with st.spinner("💬 Generating AI response..."):
        try:
            chat_completion = client.chat.completions.create(
                messages=st.session_state.chatbot_messages + [user_message],
                model=st.session_state.selected_text_model,
            )
            response = chat_completion.choices[0].message.content
        except RateLimitError:
            st.warning(f"Rate limit reached for **{st.session_state.selected_text_model}**. Please wait a moment and try again or try a different model.", icon=":material/warning:")
            st.stop()

    st.chat_message('assistant').markdown(response)
    st.session_state.chatbot_messages.append(user_message)
    st.session_state.chatbot_messages.append({'role': 'assistant', 'content': response})

elif prompt and len(prompt) > 500:
    st.warning("Prompt exceeds the 500 character limit.", icon=":material/warning:")
