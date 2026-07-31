import streamlit as st
import os

from modules.loader import load_pdf
from modules.chunker import chunk_text
from modules.embeddings import create_embeddings
from modules.vector_store import create_vector_store
from modules.retriever import retrieve_answer
from modules.generator import generate_answer


st.set_page_config(
    page_title="RAG PDF Chatbot",
    page_icon="📄",
    layout="centered"
)


st.title("📄 RAG PDF Chatbot")
st.write("Upload PDF and ask questions using AI")


# Session storage
if "processed" not in st.session_state:
    st.session_state.processed = False

if "chunks" not in st.session_state:
    st.session_state.chunks = None



# Upload PDF
uploaded_file = st.file_uploader(
    "Choose PDF",
    type="pdf"
)


if uploaded_file:

    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())


    if st.button("Process PDF"):

        with st.spinner("Processing PDF..."):

            text = load_pdf("temp.pdf")

            chunks = chunk_text(text)

            embeddings = create_embeddings(chunks)


            create_vector_store(
                chunks,
                embeddings
            )


            st.session_state.chunks = chunks
            st.session_state.processed = True


        st.success("PDF Processed Successfully ✅")



# Ask Question

question = st.text_input(
    "Ask your question"
)


if st.button("Ask AI"):

    if st.session_state.processed:

        with st.spinner("Thinking..."):

            context = retrieve_answer(
                question,
                True,
                st.session_state.chunks
            )


            answer = generate_answer(
                context,
                question
            )


        st.subheader("AI Answer")
        st.write(answer)


    else:
        st.warning("Please process PDF first.")