import os
import uuid

from flask import Flask, render_template, request, session

from modules.loader import load_pdf
from modules.chunker import chunk_text
from modules.embeddings import create_embeddings
from modules.vector_store import create_vector_store
from modules.retriever import retrieve_answer
from modules.llm import generate_answer


app = Flask(__name__)

app.secret_key = "rag-pdf-secret-key"


UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# Store data per user session
user_data = {}



def get_user_id():

    if "user_id" not in session:
        session["user_id"] = str(uuid.uuid4())

    return session["user_id"]



def process_pdf(pdf_path, user_id):

    text, scanned_pages = load_pdf(pdf_path)

    print("PDF Loaded ✅")


    chunks = chunk_text(text)

    print("Chunks:", len(chunks))


    embeddings = create_embeddings(chunks)

    print("Embeddings Ready ✅")


    vector_store = create_vector_store(
        chunks,
        embeddings,
        user_id
    )


    user_data[user_id] = {
        "chunks": chunks,
        "vector_store": vector_store,
        "uploaded_file": os.path.basename(pdf_path)
    }


    print("Vector Store Ready ✅")



@app.route("/")
def home():

    user_id = get_user_id()

    data = user_data.get(user_id, {})


    return render_template(
        "index.html",
        message=None,
        answer=None,
        uploaded_file=data.get("uploaded_file"),
        chat_history=session.get("chat_history", [])
    )



@app.route("/upload", methods=["POST"])
def upload_pdf():

    try:

        user_id = get_user_id()


        file = request.files["pdf"]


        if file.filename == "":

            return render_template(
                "index.html",
                message="Please select a PDF file ❌",
                answer=None
            )


        path = os.path.join(
            UPLOAD_FOLDER,
            file.filename
        )


        file.save(path)


        process_pdf(
            path,
            user_id
        )


        session["chat_history"] = []


        return render_template(
            "index.html",
            message=f"PDF processed successfully ✅ <br> File: {file.filename}",
            answer=None,
            uploaded_file=file.filename,
            chat_history=[]
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

    try:

        user_id = get_user_id()


        question = request.form["question"]


        data = user_data.get(user_id)


        if data is None:

            return render_template(
                "index.html",
                message="Please upload PDF first ❌",
                answer=None
            )


        context = retrieve_answer(
            question,
            data["vector_store"],
            data["chunks"],
             user_id
        )


        answer = generate_answer(
            context,
            question
        )


        history = session.get(
            "chat_history",
            []
        )


        history.append({
            "question": question,
            "answer": answer
        })


        session["chat_history"] = history



        return render_template(
            "index.html",
            message=None,
            answer=answer,
            question=question,
            uploaded_file=data.get("uploaded_file"),
            chat_history=history
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

    user_id = get_user_id()


    session.clear()


    if user_id in user_data:

        del user_data[user_id]


    return render_template(
        "index.html",
        message="New chat started ✅",
        answer=None,
        uploaded_file=None,
        chat_history=[]
    )



if __name__ == "__main__":

    app.run(debug=True)