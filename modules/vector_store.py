from modules.pinecone_db import upload_embeddings


def create_vector_store(chunks, embeddings, user_id):

    # Upload embeddings to Pinecone
    upload_embeddings(
        chunks,
        embeddings,
        user_id
    )

    return True