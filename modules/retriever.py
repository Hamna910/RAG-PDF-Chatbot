from modules.embeddings import create_embeddings
from modules.pinecone_db import search_embeddings


def retrieve_answer(query, vector_store, chunks, user_id):


    query_embedding = create_embeddings(
        [query]
    )[0]


    results = search_embeddings(
        query_embedding,
        user_id,
        top_k=3
    )


    if not results.matches:

        return None


    context = ""


    for match in results.matches:

        context += match.metadata["text"] + "\n\n"


    return context