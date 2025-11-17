import streamlit as st
from langchain_groq import ChatGroq
from langchain.agents import initialize_agent, AgentType
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
from utils.sidebar import render_sidebar
from models.active_models import get_owner
from utils.constants import wikipedia_tool_name, duckduckgo_tool_name, generic_error_message, searchbot_state
from utils.initialize import initialize

# ---------------------------------------
# Initialize session
# ---------------------------------------
initialize()

# ---------------------------------------
# Groq LLM Client
# ---------------------------------------
llm = ChatGroq(
    model=st.session_state.selected_text_model,
    temperature=0.0,
    max_retries=2,
    groq_api_key=st.secrets['groq_api_key']
)

# ---------------------------------------
# Sidebar
# ---------------------------------------
with st.sidebar:
    render_sidebar(searchbot_state)

# ---------------------------------------
# Page Header
# ---------------------------------------
st.title('🔎 Searchbot')
st.caption(f"🚀 Chatbot powered by {st.session_state.selected_text_model} ({get_owner(st.session_state.selected_text_model)}) and {st.session_state.selected_search_tool}")

st.info(
    "Some Large Language Models (LLMs) may not handle the search tool well and can produce errors. Try switching the model and tool in the sidebar.",
    icon=":material/info:"
)

# ---------------------------------------
# Chat History
# ---------------------------------------
for message in st.session_state.search_messages:
    st.chat_message(message['role']).markdown(message['content'])

# ---------------------------------------
# Prompt Input
# ---------------------------------------
prompt = st.chat_input('Ask me anything, I can search the web for you (max 500 characters)')

# ---------------------------------------
# LLM Response
# ---------------------------------------
if prompt and len(prompt) <= 500:
    st.chat_message('user').markdown(prompt)
    st.session_state.search_messages.append({ 'role': 'user', 'content': prompt })

    if st.session_state.selected_search_tool == wikipedia_tool_name:
        search_tool = st.session_state.wikipedia_tool
    elif st.session_state.selected_search_tool == duckduckgo_tool_name:
        search_tool = st.session_state.duckduckgo_tool

    search_agent = initialize_agent(
        [search_tool], llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        handle_parsing_errors=True,
        max_iterations=5
    )

    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)

        try:
            response = search_agent.run(st.session_state.search_messages, callbacks=[st_cb])
            st.session_state.search_messages.append({"role": "assistant", "content": response})
            st.write(response)
        except Exception as e:
            if "DuckDuckGoSearchException" in str(type(e)):
                message = "DuckDuckGo is currently rate-limiting the search tool. Please try again later or use another search tool."
                st.warning(message, icon="🦆")
            else:
                message = generic_error_message
                st.error(message, icon=":material/error:")

            st.session_state.search_messages.append({"role": "assistant", "content": message})

elif prompt and len(prompt) > 500:
    st.warning("Prompt exceeds the 500 character limit.", icon=":material/warning:")
