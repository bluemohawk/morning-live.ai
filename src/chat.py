from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from src.models import State

def create_chat_graph(llm_model):
    def chatbot(state: State):
        answer = llm_model.invoke(state["messages"])
        return {"messages": [answer]}

    builder = StateGraph(State)
    builder.add_node("chatbot", chatbot)
    builder.add_edge(START, "chatbot")
    builder.add_edge("chatbot", END)
    return builder.compile(checkpointer=MemorySaver())
