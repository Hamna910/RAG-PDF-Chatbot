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
    layout="wide"
)


# ===========================
# CUSTOM CSS
# ===========================

st.markdown("""
<style>

*{
    font-family: 'Poppins', sans-serif;
}


.stApp{

    background:
    linear-gradient(
        135deg,
        #020617,
        #0f172a,
        #1e1b4b
    );

    color:#e5e7eb;
}



.main-card{

    background:#111827;

    padding:30px;

    border-radius:25px;

    box-shadow:
    0 20px 50px rgba(0,0,0,.45);

}



.logo{

    width:75px;

    height:75px;

    margin:auto;

    display:flex;

    justify-content:center;

    align-items:center;

    font-size:38px;

    border-radius:20px;


    background:
    linear-gradient(
        135deg,
        #6366f1,
        #a855f7
    );

}



.title{

    text-align:center;

    color:#f8fafc;

    font-size:35px;

    font-weight:700;

}



.subtitle{

    text-align:center;

    color:#94a3b8;

}



.panel{

    background:#0f172a;

    border-radius:22px;

    padding:25px;

    border:1px solid #334155;

}



.panel-title{

    color:#a78bfa;

    font-size:22px;

    font-weight:600;

}



.card-box{

    background:#1e293b;

    padding:20px;

    border-radius:18px;

    border:1px solid #334155;

}



.success-box{

    background:#052e16;

    color:#86efac;

    padding:15px;

    border-radius:15px;

    border-left:5px solid #22c55e;

}



.answer-box{

    background:#172554;

    padding:20px;

    border-radius:18px;

    border-left:5px solid #818cf8;

}



.footer{

    text-align:center;

    margin-top:25px;

    color:#64748b;

}



</style>

""", unsafe_allow_html=True)



# ===========================
# SESSION
# ===========================

if "processed" not in st.session_state:
    st.session_state.processed = False


if "chunks" not in st.session_state:
    st.session_state.chunks = None


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []



# MAIN CARD START

st.markdown('<div class="main-card">', unsafe_allow_html=True)


st.markdown("""
<div style="text-align:center">

<div class="logo">
📄
</div>

<br>

<div class="title">
RAG PDF Chatbot
</div>

<div class="subtitle">
Chat with your PDF using AI
</div>

</div>
""", unsafe_allow_html=True)
# ===========================
# QUESTION SECTION
# ===========================

st.markdown("### 🤖 Ask AI")


question = st.text_input(
    "",
    placeholder="Ask anything from your PDF..."
)



# ===========================
# MAIN COLUMNS
# ===========================

col1, col2 = st.columns(2)



# ===========================
# LEFT DOCUMENT PANEL
# ===========================

with col1:

    st.markdown("""
    <div class="panel">

    <div class="panel-title">
    📂 Document
    </div>

    </div>
    """, unsafe_allow_html=True)



    uploaded_file = st.file_uploader(
        "📤 Choose PDF",
        type="pdf"
    )



    if uploaded_file:


        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())



        st.markdown(
            f"""
            <div class="card-box">

            <h3>📄 Current PDF</h3>

            <p>{uploaded_file.name}</p>

            </div>
            """,
            unsafe_allow_html=True
        )



        if st.button("📤 Process PDF"):


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



            st.markdown(
                """
                <div class="success-box">

                PDF Processed Successfully ✅

                </div>
                """,
                unsafe_allow_html=True
            )





# ===========================
# RIGHT CHAT PANEL
# ===========================

with col2:


    st.markdown("""
    <div class="panel">

    <div class="panel-title">
    💬 Chat
    </div>

    </div>
    """, unsafe_allow_html=True)



    if st.session_state.chat_history:


        for chat in st.session_state.chat_history:


            st.markdown(
                f"""
                <div class="card-box">

                <b>👤 You</b>

                <p>
                {chat['question']}
                </p>


                <hr>


                <b>🤖 AI</b>

                <p>
                {chat['answer']}
                </p>


                </div>

                <br>

                """,
                unsafe_allow_html=True
            )



    else:

        st.info(
            "🤖 Upload PDF and start asking questions..."
        )



# ===========================
# ASK BUTTON
# ===========================

if st.button("🤖 Ask AI"):


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



        st.session_state.chat_history.append(
            {
                "question": question,
                "answer": answer
            }
        )


        st.rerun()



    else:

        st.warning(
            "Please upload and process PDF first."
        )
        # ===========================
# FOOTER
# ===========================

st.markdown("""
<br>

<div class="footer">

Built with Streamlit • RAG • Groq LLM

</div>

""", unsafe_allow_html=True)