from modules.embeddings import create_embeddings
from modules.vector_store import search_vector_store


def retrieve_answer(query, vector_store, chunks):

    # Question ka embedding banana
    query_embedding = create_embeddings([query])

    # FAISS search
    indexes, distances = search_vector_store(
        vector_store,
        query_embedding,
        k=1
    )

    # Best matching chunk
    best_chunk = chunks[indexes[0][0]]

    return best_chunk


if __name__ == "__main__":

    print("Retriever module ready 🚀")