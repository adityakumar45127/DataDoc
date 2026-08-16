from langchain_google_genai import ChatGoogleGenerativeAI
from src.utils.env_loader import get_google_api_key


def get_llm():
    """
    Returns configured Gemini model.
    """

    llm = ChatGoogleGenerativeAI(
        model="gemini-3.6-flash",
        google_api_key=get_google_api_key(),
        temperature=0.2
    )

    return llm
llm = get_llm()