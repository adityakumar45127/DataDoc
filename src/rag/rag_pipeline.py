from src.rag.document_loader import load_pdf
from src.rag.chunker import create_chunks
from src.rag.embeddings import (
    embed_chunks,
    get_embedding_model
)

from src.rag.vector_store import (
    get_vector_store,
    add_documents,
    search_similar_documents
)

from src.rag.rag_generator import generate_rag_answer


# ==================================================
# BUILD RAG INDEX
# ==================================================

def build_rag_index(
    pdf_path,
    document_id,
    document_name
):

    # ----------------------------------------------
    # Load PDF
    # ----------------------------------------------

    documents = load_pdf(
        pdf_path
    )


    # ----------------------------------------------
    # Create chunks
    # ----------------------------------------------

    chunks = create_chunks(
        documents
    )


    if not chunks:

        raise RuntimeError(
            "No chunks were created from the PDF."
        )


    # ----------------------------------------------
    # Generate embeddings
    # ----------------------------------------------

    embedded_chunks = embed_chunks(
        chunks,
        document_id,
        document_name
    )


    if not embedded_chunks:

        raise RuntimeError(
            "Embedding generation failed. "
            "No document embeddings were created."
        )


    # ----------------------------------------------
    # Get ChromaDB collection
    # ----------------------------------------------

    collection = get_vector_store()


    if collection is None:

        raise RuntimeError(
            "Failed to create ChromaDB collection."
        )


    # ----------------------------------------------
    # Add documents to ChromaDB
    # ----------------------------------------------

    add_documents(
        collection,
        embedded_chunks
    )


    # ----------------------------------------------
    # Return collection
    # ----------------------------------------------

    return collection


# ==================================================
# ASK RAG QUESTION
# ==================================================

def ask_rag_question(
    collection,
    question,
    document_id,
    top_k=5
):

    embedding_model = get_embedding_model()

    query_embedding = embedding_model.encode(
        question
    ).tolist()

    results = search_similar_documents(
        collection,
        query_embedding,
        top_k=top_k,
        document_id=document_id
    )

    retrieved_documents = results["documents"][0]
    sources = results["metadatas"][0]

    print("\n===== RETRIEVED CONTEXT =====")

    for i, (document, source) in enumerate(
        zip(
            retrieved_documents,
            sources
        )
    ):

        print(f"\n--- Chunk {i + 1} ---")

        print(
            f"Document: {source.get('document_name')}"
        )

        print(
            f"Document ID: {source.get('document_id')}"
        )

        print(
            f"Page: {source.get('page_number')}"
        )

        print(document)

    if not retrieved_documents:

        return (
            "I could not find relevant information "
            "in the provided document.",
            []
        )

    answer = generate_rag_answer(
        question,
        retrieved_documents
    )

    return answer, sources