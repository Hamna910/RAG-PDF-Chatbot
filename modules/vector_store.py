from modules.pinecone_db import upload_embeddings


def create_vector_store(chunks, embeddings):

    # Upload embeddings to Pinecone
    upload_embeddings(chunks, embeddings)

    return True