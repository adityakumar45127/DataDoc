from pypdf import PdfReader


def load_pdf(file_path):

    reader = PdfReader(file_path)

    documents = []

    for page_number, page in enumerate(reader.pages):

        text = page.extract_text()

        if text:
            documents.append({
                "page_number": page_number + 1,
                "text": text
            })

    return documents