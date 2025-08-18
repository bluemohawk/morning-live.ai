from langchain_google_genai import ChatGoogleGenerativeAI

def create_llm(config):
    return ChatGoogleGenerativeAI(
        model=config["model_name"],
        google_api_key=config["api_key"]
    )
