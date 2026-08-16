from langchain_ollama import ChatOllama
import traceback
from src.llm.gemini_client import llm as gemini_llm


# ==================================================
# LOCAL OLLAMA MODEL
# ==================================================

local_llm = ChatOllama(
    model="llama3.2",
    temperature=0
)


# ==================================================
# CHECK WHETHER ANSWER IS A FAILURE RESPONSE
# ==================================================

def is_invalid_answer(response):

    if not response:
        return True

    answer = response.content

    if isinstance(answer, list):

        text_parts = []

        for item in answer:

            if isinstance(item, dict):

                if "text" in item:

                    text_parts.append(
                        item["text"]
                    )

            elif isinstance(item, str):

                text_parts.append(
                    item
                )

        answer = "\n".join(
            text_parts
        )

    else:

        answer = str(answer)


    answer = answer.strip().lower()


    invalid_phrases = [

        "i could not find this information",

        "i could not find this information in the provided document",

        "the information is not provided",

        "not found in the provided context",

        "cannot find this information"

    ]


    for phrase in invalid_phrases:

        if phrase in answer:

            return True


    return False


# ==================================================
# NORMAL TEXT GENERATION
# ==================================================

def generate_with_fallback(prompt):

    # ----------------------------------------------
    # Try Gemini
    # ----------------------------------------------

    try:

        print(
            "\n===== LLM PROVIDER: GEMINI ====="
        )

        gemini_response = gemini_llm.invoke(
            prompt
        )

        print(
            "Gemini response generated successfully."
        )


        if not is_invalid_answer(
            gemini_response
        ):

            return gemini_response


        print(
            "\nGemini returned an invalid/non-answer response."
        )


    except Exception as e:

        print(
            "\n===== GEMINI FAILED ====="
        )

        print(
            f"Reason: {e}"
        )


    # ----------------------------------------------
    # Fallback to Ollama
    # ----------------------------------------------

    print(
        "\n===== LLM PROVIDER: OLLAMA ====="
    )


    local_response = local_llm.invoke(
        prompt
    )


    print(
        "Ollama response generated successfully."
    )


    return local_response


# ==================================================
# STRUCTURED OUTPUT WITH FALLBACK
# ==================================================

def generate_structured_with_fallback(
    prompt,
    output_schema
):

    # ----------------------------------------------
    # Try Gemini structured output
    # ----------------------------------------------

    try:

            print(
                "\n===== STRUCTURED LLM: GEMINI ====="
            )


            structured_gemini = (
                gemini_llm.with_structured_output(
                    output_schema
                )
            )


            response = structured_gemini.invoke(
                prompt
            )


            print(
                "Gemini structured response generated successfully."
            )


            if response is not None:

                return response


    except Exception as e:

             print(
                "\n===== GEMINI STRUCTURED FAILED ====="
            )


             print(
                f"Reason: {e}"
            )


             import traceback

             traceback.print_exc()


    # ----------------------------------------------
    # Fallback to Ollama structured output
    # ----------------------------------------------

    print(
        "\n===== STRUCTURED LLM: OLLAMA ====="
    )


    try:

        structured_ollama = (
            local_llm.with_structured_output(
                output_schema
            )
        )


        response = structured_ollama.invoke(
            prompt
        )


        print(
            "Ollama structured response generated successfully."
        )


        return response


    except Exception as e:

        print(
            "\n===== OLLAMA STRUCTURED FAILED ====="
        )

        print(
            f"Reason: {e}"
        )


        raise RuntimeError(
            "Both Gemini and Ollama failed to generate "
            "structured AI insights."
        ) from e