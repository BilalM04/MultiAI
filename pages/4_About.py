import streamlit as st
from utils.sidebar import render_sidebar
from models.active_models import get_owner
from utils.initialize import initialize

# ---------------------------------------
# Initialize session
# ---------------------------------------
initialize()

# ---------------------------------------
# Sidebar
# ---------------------------------------
with st.sidebar:
    render_sidebar(4)

# ---------------------------------------
# Content
# ---------------------------------------
st.title("💬 Chatbot")
st.write(
    "A simple, general-purpose chatbot that lets you interact with a variety of open-source "
    "**Large Language Models (LLMs)** and explore how they handle different types of conversations."
)

st.title("🔎 Searchbot")
st.write(
    "Searchbot blends LLM reasoning with real-time search tools to deliver more accurate answers. "
    "The model generates search queries, retrieves results, and uses them to form responses. "
    "Currently supported search providers:"
)
st.write(
    "- **Wikipedia:** Great for factual, structured information from a trusted knowledge base.\n"
    "- **DuckDuckGo:** A fast, privacy-focused web search engine for broad internet results."
)

st.title("🎙️ Voicebot")
st.write(
    "Talk to your AI assistant hands-free. The Voicebot converts your speech to text, "
    "generates a response using an LLM, and replies back with natural-sounding audio—"
    "making conversations fully voice-driven."
)

st.title("📝 File Q&A")
st.write(
    "Upload PDF, TXT, or Markdown files and ask questions directly about their content. "
    "This feature uses **Retrieval-Augmented Generation (RAG)**, allowing the model to pull relevant "
    "information from your documents and generate accurate, context-aware answers—making it easy to "
    "interact with your files without reading everything manually."
)

st.title("👤 About the Creator")
st.write("Feel free to reach out or explore my other projects through the links below:")
st.markdown("- **Website:** [bilalm04.github.io](https://bilalm04.github.io/)\n- **GitHub:** [BilalM04](https://github.com/BilalM04)\n- **LinkedIn:** [/in/mohammadbilal7](https://www.linkedin.com/in/mohammadbilal7/)")
