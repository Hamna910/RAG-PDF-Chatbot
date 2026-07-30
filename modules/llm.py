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

    response = client.chat.completions.create(

        model="llama-3.1-8b-instant",

        messages=[
            {
                "role": "system",
                "content": """
You are a helpful AI assistant for a PDF Question Answering system.

Instructions:
- Use the provided context as the main source.
- Explain answers clearly with useful details.
- Do not add unrelated information.
- If the answer is not available in the context, say:
"I could not find this information in the document."
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

        temperature=0.3
    )

    return response.choices[0].message.content