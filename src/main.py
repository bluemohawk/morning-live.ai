import uvicorn
from src.config import load_config
from src.llm import create_llm
from src.chat import create_chat_graph
from src.api import create_app

def main():
    # Initialize components
    config = load_config()
    llm = create_llm(config)
    graph = create_chat_graph(llm)
    app = create_app(graph)
    
    # Run server
    uvicorn.run(
        app,
        host=config["host"],
        port=config["port"]
    )

if __name__ == "__main__":
    main()
