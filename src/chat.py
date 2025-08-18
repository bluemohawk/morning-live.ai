# src/chat.py
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode
from src.models import State
from src.tools import tools

# This function decides whether to continue routing to a tool or end the graph.
def should_continue(state: State) -> str:
    # Check the last message in the state for tool calls
    if state["messages"][-1].tool_calls:
        # If there are tool calls, route to the 'tools' node
        return "tools"
    # Otherwise, end the conversation turn
    return END

def create_chat_graph(llm_model):
    def chatbot(state: State):
        # The chatbot node now just calls the LLM
        response = llm_model.invoke(state["messages"])
        return {"messages": [response]}

    builder = StateGraph(State)

    # Add the chatbot node
    builder.add_node("chatbot", chatbot)

    # Add the new tool node, which executes the tools
    tool_node = ToolNode(tools)
    builder.add_node("tools", tool_node)

    # The graph always starts at the chatbot
    builder.add_edge(START, "chatbot")

    # Add the conditional edge. After the chatbot runs, the 'should_continue'
    # function will decide where to go next: the 'tools' node or 'END'.
    builder.add_conditional_edges(
        "chatbot",
        should_continue,
    )

    # After the tools are executed, the graph routes back to the chatbot
    # to process the tool's output.
    builder.add_edge("tools", "chatbot")

    return builder.compile(checkpointer=MemorySaver())
