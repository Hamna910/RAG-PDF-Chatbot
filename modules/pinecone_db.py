import os
from dotenv import load_dotenv
from pinecone import Pinecone

load_dotenv()

api_key = os.getenv("PINECONE_API_KEY")
index_name = os.getenv("PINECONE_INDEX")

pc = Pinecone(api_key=api_key)
index = pc.Index(index_name)


# NEW: Delete all previous vectors
def clear_index():
    index.delete(delete_all=True)


def upload_embeddings(chunks, embeddings):

    vectors = []

    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        vectors.append({
            "id": str(i),
            "values": embedding.tolist(),
            "metadata": {
                "text": chunk,
                "chunk_id": i
            }
        })

    index.upsert(vectors=vectors)


def search_embeddings(query_embedding, top_k=3):

    results = index.query(
        vector=query_embedding.tolist(),
        top_k=top_k,
        include_metadata=True
    )

    return results