from modules.embeddings import create_embeddings
from modules.pinecone_db import search_embeddings


def retrieve_answer(query, vector_store, chunks):

    # Question ka embedding banao
    query_embedding = create_embeddings([query])[0]

    # Pinecone search
    results = search_embeddings(
        query_embedding,
        top_k=3
    )

    # Agar kuch na mile
    if not results.matches:
        return None

    # Best matching chunks
    context = ""

    for match in results.matches:
        context += match.metadata["text"] + "\n\n"

    return context


if __name__ == "__main__":
    print("Retriever Ready ✅")