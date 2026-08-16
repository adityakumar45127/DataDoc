from src.rag.document_loader import load_pdf
from src.rag.chunker import create_chunks
from src.rag.embeddings import embed_chunks, get_embedding_model
from src.rag.vector_store import (
    get_vector_store,
    add_documents,
    search_similar_documents
)


pdf_path = "tests/sample.pdf"


documents = load_pdf(pdf_path)

chunks = create_chunks(documents)

embedded_chunks = embed_chunks(chunks)


collection = get_vector_store()


# Store chunks in ChromaDB
if collection.count() == 0:

    add_documents(
        collection,
        embedded_chunks
    )


# User question
question = "What is discussed in this document?"


# Convert question into embedding
embedding_model = get_embedding_model()

query_embedding = embedding_model.embed_query(
    question
)


# Search ChromaDB
results = search_similar_documents(
    collection,
    query_embedding,
    top_k=3
)


print("Retrieved chunks:", len(results["documents"][0]))


for i, document in enumerate(results["documents"][0]):

    print("\n--- Result", i + 1, "---")

    print("Text:")

    print(document)

    print("\nMetadata:")

    print(results["metadatas"][0][i])