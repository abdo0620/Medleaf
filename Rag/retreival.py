from Rag import db

collection=db.get_collec()

def retreive_chunks(query:str):

    results=collection.query(query_texts=query,n_results=5)["documents"][0]
    metadatas=collection.query(query_texts=query,n_results=5)["metadatas"][0]
    return results,metadatas