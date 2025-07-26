import streamlit as st
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from components.sidebar import render_sidebar
from models.active_models import get_owner
import tempfile

# App title
st.set_page_config(page_title="MultiAI", page_icon="./assets/robot.png")

# Sidebar elements
with st.sidebar:
    render_sidebar(1)

llm = ChatGroq(
    model=st.session_state.selected_model,
    temperature=0.2,
    max_retries=2,
    groq_api_key=st.secrets['groq_api_key']
)

@st.cache_resource
def load_files(file_paths):
    loaders = []
    for file_path in file_paths:
        if file_path.endswith('.pdf'):
            loaders.append(PyPDFLoader(file_path))
        elif file_path.endswith('.txt') or file_path.endswith('.md'):
            loaders.append(TextLoader(file_path, encoding='utf-8'))

    # Load documents
    all_documents = []
    for loader in loaders:
        all_documents.extend(loader.load())

    # Split
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=20)
    all_splits = text_splitter.split_documents(all_documents)

    vectorstore = FAISS.from_documents(documents=all_splits, embedding=HuggingFaceEmbeddings(model_name='all-MiniLM-L12-v2'))
    
    return vectorstore

# Page title
st.title('📝 File Q&A')
st.caption("🚀 Chatbot powered by " + st.session_state.selected_model + " (" + get_owner(st.session_state.selected_model) + ")")

def clear_context():
    st.session_state.qna_messages = []
    if 'chain' in st.session_state:
        del st.session_state.chain  # Clear the old chain if it exists

# File uploader with on_change callback to clear the context
uploaded_files = st.file_uploader("Upload PDF, TXT, or MD files", type=["pdf", "txt", "md"], accept_multiple_files=True, on_change=clear_context)

# Flag to check if any file is empty
error_detected = False

if uploaded_files:
    file_paths = []

    for uploaded_file in uploaded_files:
        if uploaded_file.size == 0:
            # If any file is empty, set the error flag and break
            error_detected = True
            break

        file_extension = uploaded_file.name.split('.')[-1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_extension}") as temp_file:
            temp_file.write(uploaded_file.read())
            file_paths.append(temp_file.name)

    if not error_detected and 'chain' not in st.session_state:
        vectorstore = load_files(file_paths)
        st.session_state.chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type='stuff',
            retriever=vectorstore.as_retriever(),
            input_key='question'
        )

# Session state message variable to hold old messages
if 'qna_messages' not in st.session_state:
    st.session_state.qna_messages = []

# Display all historical messages
for message in st.session_state.qna_messages:
    st.chat_message(message['role']).markdown(message['content'])

# Prompt input template to display the prompts
if error_detected:
    st.error("❗ One or more of the uploaded documents is empty. Please remove them and try again.")
    prompt = st.chat_input('Please remove the empty file(s) and upload valid ones', disabled=True)
elif uploaded_files:
    prompt = st.chat_input('Ask a question about the uploaded file (max 500 characters)', disabled=False)
else:
    prompt = st.chat_input('Please upload a file', disabled=True)

# Ensure the prompt is within the character limit
if prompt and len(prompt) <= 500:
    # Display the prompt
    st.chat_message('user').markdown(prompt)

    # Store user prompt in state
    st.session_state.qna_messages.append({'role': 'user', 'content': prompt})
    
    # Get response from the LLM using RAG
    response = st.session_state.chain.run(prompt)
    
    # Show the LLM response
    st.chat_message('assistant').markdown(response)

    # Store the LLM response in state
    st.session_state.qna_messages.append({'role': 'assistant', 'content': response})
elif prompt and len(prompt) > 500:
    st.warning("⚠️ Prompt exceeds the 500 character limit.")
