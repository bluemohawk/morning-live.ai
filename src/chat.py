# src/chat.py
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
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
    # System prompt to instruct the agent
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful assistant. Please respond to the user's request only based on the given context.",
            ),
            ("placeholder", "{messages}"),
        ]
    )
    # Create the tool-calling agent
    chatbot = create_tool_calling_agent(llm_model, tools, prompt)

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
