from src.rag.document_loader import load_pdf
from src.rag.chunker import create_chunks
from src.rag.embeddings import embed_chunks, get_embedding_model
from src.rag.vector_store import (
    get_vector_store,
    add_documents,
    search_similar_documents
)
from src.rag.rag_generator import generate_rag_answer


pdf_path = "tests/sample.pdf"


# Load PDF
documents = load_pdf(pdf_path)

# Create chunks
chunks = create_chunks(documents)

# Generate embeddings
embedded_chunks = embed_chunks(chunks)

# Get ChromaDB collection
collection = get_vector_store()


# Add documents if collection is empty
if collection.count() == 0:

    add_documents(
        collection,
        embedded_chunks
    )


# User question
question = "What is discussed in this document?"


# Embed question
embedding_model = get_embedding_model()

query_embedding = embedding_model.embed_query(
    question
)


# Retrieve relevant chunks
results = search_similar_documents(
    collection,
    query_embedding,
    top_k=3
)


# Extract retrieved text
retrieved_documents = results["documents"][0]


# Generate answer using Gemini
answer = generate_rag_answer(
    question,
    retrieved_documents
)


print("\n===== RAG ANSWER =====\n")

print(answer)