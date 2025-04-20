from langchain_google_genai import ChatGoogleGenerativeAI
from constants import GOOGLE_API_KEY

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.1
)
