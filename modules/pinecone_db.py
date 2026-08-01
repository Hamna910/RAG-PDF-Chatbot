import os
from dotenv import load_dotenv
from pinecone import Pinecone

load_dotenv()

api_key = os.getenv("PINECONE_API_KEY")
index_name = os.getenv("PINECONE_INDEX")

pc = Pinecone(api_key=api_key)

index = pc.Index(index_name)



def clear_index():

    index.delete(delete_all=True)



def upload_embeddings(chunks, embeddings, user_id):

    vectors = []


    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):

        vectors.append({

            "id": f"{user_id}-{i}",

            "values": embedding.tolist(),

            "metadata": {

                "text": chunk,

                "chunk_id": i,

                "user_id": user_id

            }

        })


    index.upsert(
        vectors=vectors
    )



def search_embeddings(query_embedding, user_id, top_k=3):


    results = index.query(

        vector=query_embedding.tolist(),

        top_k=top_k,

        include_metadata=True,

        filter={

            "user_id": {

                "$eq": user_id

            }

        }

    )


    return results