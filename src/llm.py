# src/llm.py
from langchain_google_genai import ChatGoogleGenerativeAI
from src.tools import tools # Import the tools

def create_llm(config):
    llm = ChatGoogleGenerativeAI(
        model=config["model_name"],
        google_api_key=config["api_key"]
    )
    # Bind the tools to the LLM so it knows when to call them
    return llm.bind_tools(tools)
