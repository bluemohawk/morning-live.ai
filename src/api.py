from fastapi import FastAPI
from langchain_core.messages import HumanMessage
from src.models import ChatRequest

def create_app(graph):
    app = FastAPI(
        title="LangGraph Chat API",
        description="A simple chat API using LangGraph and Gemini",
        version="1.0.0"
    )

    @app.post("/chat", 
              summary="Send a message to the chatbot",
              response_description="The chatbot's response")
    async def chat_endpoint(request: ChatRequest):
        """
        Send a message to the chatbot and get a response.
        
        Parameters:
            request: ChatRequest containing the message and optional session_id
            
        Returns:
            dict: Contains the AI's response and conversation history
        """
        input_data = {
            "messages": [HumanMessage(request.message)],
            "session_id": request.session_id
        }
        config = {"configurable": {"thread_id": request.session_id}}
        response = await graph.ainvoke(input_data, config=config)

        # Get the last message (most recent AI response)
        ai_message = response['messages'][-1]
        
        # Create response dictionary
        response_dict = {
            "response": ai_message.content,
            "session_id": request.session_id,
            "history": [
                {"role": "user" if i % 2 == 0 else "assistant", "content": msg.content}
                for i, msg in enumerate(response['messages'])
            ]
        }
        
        # Print formatted conversation history
        print("\n=== Conversation History ===")
        for msg in response_dict["history"]:
            role = msg["role"].upper()
            content = msg["content"]
            print(f"\n{role}: {content}")
            
        return response_dict

    return app
