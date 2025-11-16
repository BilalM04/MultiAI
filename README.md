# MultiAI

MultiAI is a multi-mode AI app offering four core capabilities:

- **Chatbot** for general conversations
- **Searchbot** for LLM-powered web search
- **Voicebot** for fully voice-driven conversations
- **File Q&A** for interacting with documents using Retrieval-Augmented Generation (RAG)

**Explore MultiAI at:** https://multi-ai.streamlit.app/

<div align="center">

![chatbot](https://github.com/user-attachments/assets/3c111c72-0ad2-427a-aa24-a0334da3a0db)
![searchbot](https://github.com/user-attachments/assets/f5ecce3d-a19a-4181-a2e2-316a7721b7ba)

</div>

## Features

### 💬 Chatbot

A simple, general-purpose chatbot that lets you interact with a variety of open-source **Large Language Models (LLMs)** and explore how they handle different types of conversations.

### 🔎 Searchbot

Searchbot blends LLM reasoning with real-time search tools to deliver more accurate answers. The model generates search queries, retrieves results, and uses them to form responses. Currently supported search providers:

- **Wikipedia:** Great for factual, structured information from a trusted knowledge base.
- **DuckDuckGo:** A fast, privacy-focused web search engine for broad internet results.

### 🎙️ Voicebot

Talk to your AI assistant hands-free. The Voicebot converts your speech to text, generates a response using an LLM, and replies back with natural-sounding audio—making conversations fully voice-driven.

### 📝 File Q&A

Upload PDF, TXT, or Markdown files and ask questions directly about their content. This feature uses **Retrieval-Augmented Generation (RAG)**, allowing the model to pull relevant information from your documents and generate accurate, context-aware answers—making it easy to interact with your files without reading everything manually.

## Technologies Used

### Programming Language

- **Python:** The entire app is developed in Python.

### Frontend

- **Streamlit:** Used to build the app's user interface.
  
### Large Language Models (LLMs)

- **Groq:** Provides the LLMs for chatbot responses, search queries, and file-based Q&A.

### Backend

- **LangChain:**
  - **LangChain Core:** Manages LLMs and tool interactions.
  - **LangChain Agents:** Used for `ZERO_SHOT_REACT_DESCRIPTION` agents with web search tools.
  - **LangChain Community Tools:** Integrates DuckDuckGo and Wikipedia for real-time web searches.
  - **LangChain Document Loaders:** Loads and processes PDF, TXT, and Markdown files.
  - **LangChain VectorStores:** FAISS is used for document embedding and retrieval.

### Data Processing

- **HuggingFace Embeddings:** Utilizes `all-MiniLM-L12-v2` for embedding text data in the File Q&A feature.

### File Handling

- **Tempfile:** Manages temporary storage during file uploads.

## Getting Started

### Prerequisites

- Python 3.x
- Required Python libraries (see `requirements.txt`)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/BilalM04/MultiAI.git
   ```
2. Navigate to the porject directory:
   ```bash
   cd MultiAI
   ```
3. Install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```

### Running the App

1. Start the app:
   ```bash
   streamlit run Chatbot.py
   ```
2. Open your browser and go to the `localhost` link specified in the command line.

## Usage

- **Chatbot:** Start a conversation by typing in the input field and pressing Enter.
- **SearchBot:** Type your prompt, and the bot will use both LLMs and search tools to give you an answer.
- **Voicebot:** Record or upload audio, get it transcribed, receive an LLM reply, and hear the response.
- **File Q&A:** Upload a PDF, TXT, or MD file and ask questions related to its content.

## Demo

Explore the live demo: [MultiAI](https://multi-ai.streamlit.app/)
