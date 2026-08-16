import chromadb


def get_vector_store():

    client = chromadb.PersistentClient(
        path="data/chroma_db"
    )

    collection = client.get_or_create_collection(
        name="datadoc_documents"
    )

    return collection 


def reset_vector_store():

    client = chromadb.PersistentClient(
        path="data/chroma_db"
    )

    try:
        client.delete_collection(
            name="datadoc_documents"
        )
    except Exception:
        pass

    collection = client.get_or_create_collection(
        name="datadoc_documents"
    )

    return collection


def add_documents(collection, embedded_chunks):

    documents = []
    embeddings = []
    metadatas = []
    ids = []

    for index, chunk in enumerate(embedded_chunks):

        documents.append(chunk["text"])

        embeddings.append(chunk["embedding"])

        metadatas.append({
            "document_id": chunk["document_id"],
            "document_name": chunk["document_name"],
            "page_number": chunk["page_number"]
        })

        ids.append(f"{chunk['document_id']}_chunk_{index}")

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )

def search_similar_documents(
    collection,
    query_embedding,
    top_k=3,
    document_id=None
):

    query_kwargs = {
        "query_embeddings": [query_embedding],
        "n_results": top_k
    }

    if document_id is not None:

        query_kwargs["where"] = {
            "document_id": document_id
        }

    results = collection.query(
        **query_kwargs
    )

    return results