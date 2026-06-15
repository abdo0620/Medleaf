import chromadb as db 

client=db.PersistentClient("Vectordb")
collection =client.get_collection("mrooc")
print(str(collection.query(query_texts="assurance",n_results=1)["documents"]))