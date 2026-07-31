from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()


client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_answer(context, question):

    prompt = f"""
You are an AI assistant.
Answer the user's question using the provided context.

Context:
{context}

Question:
{question}

Answer clearly:
"""


    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )


    return response.choices[0].message.content