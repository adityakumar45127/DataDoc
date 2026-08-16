from src.rag.document_loader import load_pdf
from src.rag.chunker import create_chunks
from src.rag.embeddings import embed_chunks
from src.rag.vector_store import get_vector_store, add_documents


pdf_path = "tests/sample.pdf"


documents = load_pdf(pdf_path)

chunks = create_chunks(documents)

embedded_chunks = embed_chunks(chunks)


collection = get_vector_store()


add_documents(
    collection,
    embedded_chunks
)


print("Documents added successfully!")

print("Collection name:", collection.name)

print("Number of documents:", collection.count())