import os

from modules.pinecone_db import clear_index
from flask import Flask, render_template, request

from modules.loader import load_pdf
from modules.chunker import chunk_text
from modules.embeddings import create_embeddings
from modules.vector_store import create_vector_store
from modules.retriever import retrieve_answer
from modules.llm import generate_answer


app = Flask(__name__)


UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# Global variables
chunks = []
vector_store = None
uploaded_file_name = None
chat_history = []



def process_pdf(pdf_path):

    global chunks, vector_store

    # Load PDF
    text, scanned_pages = load_pdf(pdf_path)

    print("PDF Loaded ✅")

    # Chunking
    chunks = chunk_text(text)

    print("Chunks:", len(chunks))

    # Embeddings
    embeddings = create_embeddings(chunks)

    print("Embeddings Ready ✅")

    # Clear previous vectors from Pinecone
    # clear_index()

    print("Old Pinecone vectors deleted ✅")

    # Upload new vectors to Pinecone
    vector_store = create_vector_store(
        chunks,
        embeddings
    )

    print("Vector Store Ready ✅")



@app.route("/")
def home():

   return render_template(
    "index.html",
    message=None,
    answer=None,
    chat_history=chat_history
)
@app.route("/upload", methods=["POST"])
def upload_pdf():

    global uploaded_file_name

    try:

        file = request.files["pdf"]

        if file.filename == "":
            return render_template(
                "index.html",
                message="Please select a PDF file ❌",
                answer=None
            )


        uploaded_file_name = file.filename


        path = os.path.join(
            UPLOAD_FOLDER,
            file.filename
        )

        file.save(path)


        process_pdf(path)


        return render_template(
            "index.html",
            message=f"PDF processed successfully ✅ <br> File: {uploaded_file_name}",
            answer=None,
            uploaded_file=uploaded_file_name
        )


    except Exception as e:

        print("Upload Error:", e)

        return render_template(
            "index.html",
            message="PDF processing failed ❌",
            answer=None
        )
    
@app.route("/ask", methods=["POST"])
def ask_question():

    global vector_store

    try:

        question = request.form["question"]


        if vector_store is None:

            return render_template(
                "index.html",
                message="Please upload PDF first ❌",
                answer=None
            )


        context = retrieve_answer(
            question,
            vector_store,
            chunks
        )


        answer = generate_answer(
            context,
            question
        )
        chat_history.append({
    "question": question,
    "answer": answer
})


        return render_template(
    "index.html",
    message=None,
    answer=answer,
    question=question,
    uploaded_file=uploaded_file_name,
    chat_history=chat_history
)


    except Exception as e:

        print("Question Error:", e)

        return render_template(
            "index.html",
            message="Something went wrong ❌",
            answer=None
        )

@app.route("/clear")
def clear_chat():

    global chat_history, uploaded_file_name, chunks, vector_store

    chat_history.clear()

    uploaded_file_name = None
    chunks = []
    vector_store = None


    return render_template(
        "index.html",
        message="New chat started ✅",
        answer=None,
        question="",
        uploaded_file=None,
        chat_history=chat_history
    )

if __name__ == "__main__":

    app.run(debug=True)



