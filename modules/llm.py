import os
from dotenv import load_dotenv
from groq import Groq


# Load .env file
load_dotenv()


# Initialize Groq client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_answer(context, question):

    # Agar Pinecone se koi context na mile
    if context is None or context.strip() == "":
        return "I could not find this information in the uploaded PDF."

    response = client.chat.completions.create(

        model="llama-3.1-8b-instant",

        messages=[

            {
                "role": "system",
                "content": """
You are a helpful AI assistant for a PDF Question Answering System.

Rules:

1. Answer ONLY using the provided context.
2. Never use your own knowledge.
3. If the answer is missing from the context, reply exactly:
"I could not find this information in the uploaded PDF."
4. Keep answers clear and easy to understand.
5. Do not guess or hallucinate.
"""
            },

            {
                "role": "user",
                "content": f"""
Context:
{context}

Question:
{question}

Answer:
"""
            }

        ],

        temperature=0

    )

    return response.choices[0].message.content