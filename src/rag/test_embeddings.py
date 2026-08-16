from src.rag.document_loader import load_pdf
from src.rag.chunker import create_chunks
from src.rag.embeddings import embed_chunks


pdf_path = "tests/sample.pdf"


documents = load_pdf(pdf_path)

chunks = create_chunks(documents)

embedded_chunks = embed_chunks(chunks)


print("Pages:", len(documents))

print("Chunks:", len(chunks))

print("Embedded chunks:", len(embedded_chunks))


if embedded_chunks:

    first_chunk = embedded_chunks[0]

    print("\nPage:", first_chunk["page_number"])

    print("\nText:")

    print(first_chunk["text"])

    print("\nVector dimensions:")

    print(len(first_chunk["embedding"]))

    print("\nFirst 10 vector values:")

    print(first_chunk["embedding"][:10])