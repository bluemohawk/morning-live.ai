from typing import Dict, Any
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint import BaseCheckpointer
from src.models import State

class MemoryCheckpointer(BaseCheckpointer):
    def __init__(self):
        self.states: Dict[str, Any] = {}

    async def persist(self, key: str, state: Dict[str, Any]) -> None:
        self.states[key] = state

    async def load(self, key: str) -> Dict[str, Any]:
        return self.states.get(key, {})

    async def list_keys(self) -> list[str]:
        return list(self.states.keys())

    async def delete(self, key: str) -> None:
        self.states.pop(key, None)

def create_chat_graph(llm_model):
    # Store conversation history with checkpointer
    checkpointer = MemoryCheckpointer()
    
    async def chatbot(state: State):
        # Load existing history or create new
        session_id = state.get("session_id", "default")
        history = await checkpointer.load(session_id)
        conversation_history = history.get("messages", [])
        
        # Add the new user message to history
        conversation_history.extend(state["messages"])
        
        # Use full conversation history for context
        answer = llm_model.invoke(conversation_history)
        
        # Add AI's response to history
        conversation_history.append(answer)
        
        # Save updated history
        await checkpointer.persist(session_id, {"messages": conversation_history})
        
        print(f"\n=== Session: {session_id} ===")
        print(f"History length: {len(conversation_history)}")
        print(f"Last user message: {state['messages'][-1].content}")
        print(f"AI response: {answer.content}")
        
        return {"messages": conversation_history}

    builder = StateGraph(State)
    builder.add_node("chatbot", chatbot)
    builder.add_edge(START, "chatbot")
    builder.add_edge("chatbot", END)
    
    # Set the checkpointer
    graph = builder.compile()
    graph.set_checkpointer(checkpointer)
    
    return graph
