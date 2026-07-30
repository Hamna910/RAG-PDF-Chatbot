import faiss
import numpy as np


def create_vector_store(embeddings):

    embeddings = np.array(embeddings).astype("float32")

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)

    return index


def search_vector_store(index, query_embedding, k=1):

    query_embedding = np.array(query_embedding).astype("float32")

    distances, indexes = index.search(
        query_embedding,
        k
    )

    return indexes, distances


if __name__ == "__main__":

    sample_embeddings = np.array([
        [0.1, 0.2, 0.3],
        [0.4, 0.5, 0.6]
    ]).astype("float32")


    store = create_vector_store(sample_embeddings)

    print("Total vectors:", store.ntotal)