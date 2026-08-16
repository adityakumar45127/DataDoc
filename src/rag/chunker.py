from langchain_text_splitters import RecursiveCharacterTextSplitter


def create_chunks(documents):

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )

    chunks = []

    for document in documents:

        split_texts = text_splitter.split_text(
            document["text"]
        )

        for chunk in split_texts:

            chunks.append({
                "page_number": document["page_number"],
                "text": chunk
            })

    return chunks