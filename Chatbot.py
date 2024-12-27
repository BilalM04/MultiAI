import streamlit as st
from groq import Groq
from components.sidebar import render_sidebar
from models.active_models import get_owner

# App title
st.set_page_config(page_title="MultiAI", page_icon="./assets/robot.png")

# Sidebar elements
with st.sidebar:
    render_sidebar(0)

# Initialize the Groq client
client = Groq(api_key=st.secrets["groq_api_key"])

# Page title
st.title('💬 Chatbot')
st.caption("🚀 Chatbot powered by " + st.session_state.selected_model + " (" + get_owner(st.session_state.selected_model) + ")")

# Session state message variable to hold old messages
if 'chatbot_messages' not in st.session_state:
    st.session_state.chatbot_messages = []

# Display all historical messages
for message in st.session_state.chatbot_messages:
    st.chat_message(message['role']).markdown(message['content'])

# Prompt input template to display the prompts
prompt = st.chat_input('Pass your prompt here (max 500 characters).')

# Ensure the prompt is within the character limit
if prompt and len(prompt) <= 500:
    # Display the prompt
    st.chat_message('user').markdown(prompt)
    # Store user prompt in state
    st.session_state.chatbot_messages.append({'role':'user', 'content':prompt})
    
    # Get response from the LLM
    chat_completion = client.chat.completions.create(
        messages=st.session_state.chatbot_messages + [{"role": "user", "content": prompt}],
        model=st.session_state.selected_model,
    )
    response = chat_completion.choices[0].message.content
    
    # Show the LLM response
    st.chat_message('assistant').markdown(response)
    # Store the LLM response in state
    st.session_state.chatbot_messages.append({'role': 'assistant', 'content': response})
elif prompt and len(prompt) > 500:
    st.warning("⚠️ Prompt exceeds the 500 character limit.")
