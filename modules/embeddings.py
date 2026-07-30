from sentence_transformers import SentenceTransformer


# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def create_embeddings(chunks):
    embeddings = model.encode(chunks)

    return embeddings


if __name__ == "__main__":

    sample_chunks = [
        "Artificial intelligence is the future.",
        "Python is used for machine learning."
    ]

    result = create_embeddings(sample_chunks)

    print("Embedding Shape:", result.shape)