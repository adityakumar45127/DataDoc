from src.llm.llm_router import generate_with_fallback
from src.rag.rag_prompt import RAG_PROMPT


def generate_rag_answer(
    question,
    retrieved_documents
):

    # ----------------------------------------------
    # Combine retrieved chunks
    # ----------------------------------------------

    context = "\n\n".join(
        retrieved_documents
    )


    # ----------------------------------------------
    # Build RAG prompt
    # ----------------------------------------------

    prompt = RAG_PROMPT.format(
        context=context,
        question=question
    )


    # ----------------------------------------------
    # Generate answer
    # ----------------------------------------------

    response = generate_with_fallback(
        prompt
    )


    # ----------------------------------------------
    # Extract response text
    # ----------------------------------------------

    if isinstance(
        response.content,
        str
    ):

        return response.content


    if isinstance(
        response.content,
        list
    ):

        text_parts = []

        for item in response.content:

            if isinstance(
                item,
                dict
            ):

                if "text" in item:

                    text_parts.append(
                        item["text"]
                    )

            elif isinstance(
                item,
                str
            ):

                text_parts.append(
                    item
                )

        return "\n".join(
            text_parts
        )


    return str(
        response.content
    )