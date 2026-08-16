from src.rag.document_loader import load_pdf
from src.rag.chunker import create_chunks


pdf_path = "tests/sample.pdf"

documents = load_pdf(pdf_path)

chunks = create_chunks(documents)

print("Pages:", len(documents))

print("Chunks:", len(chunks))

if chunks:
    print("\nFirst chunk:\n")
    print(chunks[0]["text"])
    print("\nPage:", chunks[0]["page_number"])