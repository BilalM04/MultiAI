import streamlit as st
from components.sidebar import render_sidebar
from models.active_models import get_owner

# App title
st.set_page_config(page_title="MultiAI", page_icon="./assets/robot.png")

# Render the sidebar 
with st.sidebar:
    render_sidebar(3)

# About Chatbot
st.title("💬 Chatbot")
st.write("This is just a regular chatbot where you can interact with various open source **Large Language Models** (LLMs). Whether you want to ask questions, chat about random topics, or just explore what these models can do, this chatbot is here to help. It's a fun and simple way to see how LLMs handle different kinds of conversations.")

# About SearchBot
st.title("🔎 SearchBot")
st.write("SearchBot is a bit more advanced. It combines the power of LLMs with search tools, like DuckDuckGo's LangChain Python modules, to give you more accurate answers. The LLMs generate search queries, and then the results are used to build responses. Not all LLMs are great at using these search tools, so you might see some errors occasionally. Below is a list of LLMs that most consistently perform well with the search tool:")

consistent_llms = ["llama3-70b-8192", "llama3-8b-8192", "gemma2-9b-it", "mistral-saba-24b"]

# About File Q&A
st.markdown("\n".join([f"- {llm} ({get_owner(llm)})" for llm in consistent_llms]))

st.title("📝 File Q&A")
st.write("With the File Q&A feature, you can upload files in PDF, TXT, or Markdown (MD) formats and ask questions based on the content of those files. The LLMs use **Retrieval-Augmented Generation** (RAG), which means they retrieve relevant information from the document and generate answers that are contextually accurate. This approach helps the model provide more precise responses based on the actual content of the files, making it a handy way to interact with your documents without having to read through everything yourself.")

# About Creator
st.title("👤 About the Creator")
st.write("Feel free to reach out or explore my other projects through the links below:")
st.markdown("- **Website:** [bilalm04.github.io](https://bilalm04.github.io/)\n- **GitHub:** [BilalM04](https://github.com/BilalM04)\n- **LinkedIn:** [/in/mohammadbilal7](https://www.linkedin.com/in/mohammadbilal7/)")
