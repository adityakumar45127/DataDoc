from sentence_transformers import SentenceTransformer


_embedding_model = None


def get_embedding_model():

    global _embedding_model

    if _embedding_model is None:

        _embedding_model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    return _embedding_model


def embed_chunks(
    chunks,
    document_id,
    document_name
):

    embedding_model = get_embedding_model()

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    print(
        f"Generating embeddings for "
        f"{len(texts)} chunks..."
    )

    vectors = embedding_model.encode(
        texts,
        show_progress_bar=True,
        convert_to_numpy=True
    )

    embedded_chunks = []

    for chunk, vector in zip(
        chunks,
        vectors
    ):

        embedded_chunks.append({

            "document_id": document_id,

            "document_name": document_name,

            "page_number": chunk["page_number"],

            "text": chunk["text"],

            "embedding": vector.tolist()

        })

    if not embedded_chunks:

        raise RuntimeError(
            "No embeddings were generated."
        )

    print(
        f"Successfully generated "
        f"{len(embedded_chunks)} embeddings."
    )

    return embedded_chunks