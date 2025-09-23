# MultiAI

This app provides three main features: a standard Chatbot for general conversations, a more advanced SearchBot that leverages Large Language Models (LLMs) with search tools, and a File Q&A feature that allows you to interact with documents by asking questions based on their content.

**Explore MultiAI at:** https://multi-ai.streamlit.app/

<div align="center">

![chatbot](https://github.com/user-attachments/assets/3c111c72-0ad2-427a-aa24-a0334da3a0db)
![searchbot](https://github.com/user-attachments/assets/f5ecce3d-a19a-4181-a2e2-316a7721b7ba)

</div>

## Features

### 💬 Chatbot

This is just a regular chatbot where you can interact with various open source Large Language Models (LLMs). Whether you want to ask questions, chat about random topics, or just explore what these models can do, this chatbot is here to help. It's a fun and simple way to see how LLMs handle different kinds of conversations.

### 🔎 SearchBot

SearchBot is a bit more advanced. It combines the power of LLMs with search tools, like DuckDuckGo's LangChain Python modules, to give you more accurate answers. The LLMs generate search queries, and then the results are used to build responses. Not all LLMs are great at using these search tools, so you might see some errors occasionally. Check the 'About' page for a list of LLMs that most consistently perform well with the search tool.

### 📝 File Q&A

With the File Q&A feature, you can upload files in PDF, TXT, or Markdown (MD) formats and ask questions based on the content of those files. The LLMs use Retrieval-Augmented Generation (RAG), which means they retrieve relevant information from the document and generate answers that are contextually accurate. This approach helps the model provide more precise responses based on the actual content of the files, making it a handy way to interact with your documents without having to read through everything yourself.

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
  - **LangChain Community Tools:** Integrates DuckDuckGo for real-time web searches.
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
- **File Q&A:** Upload a PDF, TXT, or MD file and ask questions related to its content.

## Demo

Explore the live demo: [MultiAI](https://multi-ai.streamlit.app/)
