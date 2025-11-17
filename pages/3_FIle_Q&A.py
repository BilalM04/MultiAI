import streamlit as st
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from utils.sidebar import render_sidebar
from utils.initialize import initialize
from utils.constants import fileqna_state
from models.active_models import get_owner
import tempfile

# ---------------------------------------
# Initialize session
# ---------------------------------------
initialize()

# ---------------------------------------
# Groq LLM Client
# ---------------------------------------
llm = ChatGroq(
    model=st.session_state.selected_text_model,
    temperature=0.2,
    max_retries=2,
    groq_api_key=st.secrets['groq_api_key']
)

# ---------------------------------------
# Clear context
# ---------------------------------------
def clear_context():
    st.session_state.qna_messages = []
    if 'chain' in st.session_state:
        del st.session_state.chain

# ---------------------------------------
# Load files and store as vectorestore
# ---------------------------------------
@st.cache_resource
def load_files(file_paths):
    loaders = []
    for file_path in file_paths:
        if file_path.endswith('.pdf'):
            loaders.append(PyPDFLoader(file_path))
        elif file_path.endswith('.txt') or file_path.endswith('.md'):
            loaders.append(TextLoader(file_path, encoding='utf-8'))

    all_documents = []
    for loader in loaders:
        all_documents.extend(loader.load())

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=20)
    all_splits = text_splitter.split_documents(all_documents)

    vectorstore = FAISS.from_documents(documents=all_splits, embedding=HuggingFaceEmbeddings(model_name='all-MiniLM-L12-v2'))
    
    return vectorstore

# ---------------------------------------
# Sidebar
# ---------------------------------------
with st.sidebar:
    render_sidebar(fileqna_state)

# ---------------------------------------
# Page Header
# ---------------------------------------
st.title('📝 File Q&A')
st.caption("🚀 Chatbot powered by " + st.session_state.selected_text_model + " (" + get_owner(st.session_state.selected_text_model) + ")")

# ---------------------------------------
# File Uploader
# ---------------------------------------
uploaded_files = st.file_uploader(
    "Upload PDF, TXT, or MD files",
    type=["pdf", "txt", "md"],
    accept_multiple_files=True,
    on_change=clear_context
)
empty_file = False

# ---------------------------------------
# Process uploaded files and initialize 
# RAG pipeline
# ---------------------------------------
if uploaded_files:
    file_paths = []

    for uploaded_file in uploaded_files:
        if uploaded_file.size == 0:
            empty_file = True
            break

        file_extension = uploaded_file.name.split('.')[-1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_extension}") as temp_file:
            temp_file.write(uploaded_file.read())
            file_paths.append(temp_file.name)

    if not empty_file and 'chain' not in st.session_state:
        vectorstore = load_files(file_paths)
        st.session_state.chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type='stuff',
            retriever=vectorstore.as_retriever(),
            input_key='question'
        )

# ---------------------------------------
# Chat History
# ---------------------------------------
for message in st.session_state.qna_messages:
    st.chat_message(message['role']).markdown(message['content'])

# ---------------------------------------
# Prompt Input
# ---------------------------------------
if empty_file:
    st.error("One or more of the uploaded documents is empty. Please remove them and try again.", icon=":material/error:")
    prompt = st.chat_input('Please remove the empty file(s) and upload valid ones', disabled=True)
elif uploaded_files:
    prompt = st.chat_input('Ask a question about the uploaded file (max 500 characters)', disabled=False)
else:
    prompt = st.chat_input('Please upload a file', disabled=True)

# ---------------------------------------
# LLM Response using RAG
# ---------------------------------------
if prompt and len(prompt) <= 500:
    st.chat_message('user').markdown(prompt)
    st.session_state.qna_messages.append({'role': 'user', 'content': prompt})
    
    # Get response from the LLM using RAG
    response = st.session_state.chain.run(prompt)
    
    st.chat_message('assistant').markdown(response)
    st.session_state.qna_messages.append({'role': 'assistant', 'content': response})
elif prompt and len(prompt) > 500:
    st.warning("Prompt exceeds the 500 character limit.", icon=":material/warning:")
