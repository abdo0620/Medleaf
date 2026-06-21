import chromadb as db 

client=db.PersistentClient("Vectordb")
collection =client.get_collection("mrooc")

def retreive_chunks(query:str):

    results=collection.query(query_texts=query,n_results=5)["documents"]
    return results