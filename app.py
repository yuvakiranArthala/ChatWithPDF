import os
import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader

from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain

from templetes import css, bot_templete, user_templete

load_dotenv()

def get_pdf_text(pdf_files):
    text = ""
    for pdf in pdf_files:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_vector_stores(text_chunks):
    embeddings = OpenAIEmbeddings(openai_api_key=os.environ['OPENAI_API_KEY'])
    vector_store = FAISS.from_texts(texts=text_chunks, embedding=embeddings)

    return vector_store

def get_text_chunks(raw_text):
    text_splitter =  CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )

    chunks = text_splitter.split_text(raw_text)
    return chunks

def get_conversation_chain(vector_store):
    llm = ChatOpenAI()
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vector_store.as_retriever(),
        memory=memory
    )

    return conversation_chain

def handle_user_input(user_input):
    response = st.session_state.conversation({'question': user_input})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_templete.replace("{{msg}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_templete.replace("{{msg}}", message.content), unsafe_allow_html=True)

def main():
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.set_page_config(page_title="Chat With PDFs", page_icon=":book:")
    st.write(css, unsafe_allow_html=True)
    st.header("Chat With PDFs :books:")
    user_query = st.text_input('Query about your document')
    if user_query:
        handle_user_input(user_query)

    st.write(user_templete.replace("{{msg}}", "hello bot"), unsafe_allow_html=True)
    st.write(bot_templete.replace("{{msg}}", "hello human"), unsafe_allow_html=True)

    with st.sidebar:
        st.subheader("Your Documents")
        pdf_docs = st.file_uploader("Upload your PDFs", accept_multiple_files=True)
        
        if st.button("Process"):
            with st.spinner("Processing"):
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                vector_store =  get_vector_stores(text_chunks)
                st.session_state.conversation = get_conversation_chain(vector_store)
    
if __name__ == '__main__':
    main()