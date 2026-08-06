from src.llm.gemini_client import get_llm

llm = get_llm()

response = llm.invoke(
    "Introduce yourself as DataDoc AI in exactly two sentences."
)

print(response.content)