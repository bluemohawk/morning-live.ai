import pytest
from unittest.mock import patch, MagicMock
from src.chat import create_chat_graph
from src.llm import create_llm
from src.config import load_config
from langchain_core.messages import HumanMessage
from langgraph.graph.message import AnyMessage

@pytest.fixture
def config():
    return {
        "model_name": "gemini-1.5-flash",
        "api_key": "test_key",
        "host": "0.0.0.0",
        "port": 8000,
    }

@pytest.fixture
def llm(config):
    return create_llm(config)

@pytest.fixture
def chat_graph(llm):
    return create_chat_graph(llm)

@patch('langchain_community.tools.tavily_search.TavilySearchResults.invoke')
def test_chat_graph_tool_call(mock_tavily_invoke, chat_graph):
    # Mock the tool's response
    mock_tavily_invoke.return_value = "The weather in Paris is sunny."

    # Define the input for the graph
    inputs = {"messages": [HumanMessage(content="what is the weather in paris?")]}

    # Create a mock for the LLM's response to simulate a tool call
    mock_tool_call = MagicMock()
    mock_tool_call.tool_calls = [{"name": "tavily_search", "args": {"query": "weather in Paris"}, "id": "tool_call_123"}]

    # We need to patch the invoke method of the llm_model inside create_chat_graph
    # to control the response and simulate a tool call
    with patch('langchain_google_genai.ChatGoogleGenerativeAI.invoke', return_value=mock_tool_call) as mock_llm_invoke:
        # Run the graph
        result = chat_graph.invoke(inputs, {"configurable": {"session_id": "test-session"}})

        # 1. Assert that the LLM was called with the initial message
        mock_llm_invoke.assert_any_call([HumanMessage(content="what is the weather in paris?")])

        # 2. Assert that the Tavily tool was called with the correct query
        mock_tavily_invoke.assert_called_once_with({'query': 'weather in Paris'})

        # 3. Assert that the final response contains the tool's output
        # The result will contain a list of messages, including the tool's output
        # We need to find the message that contains the tool's output
        messages = result.get("messages", [])
        assert any("The weather in Paris is sunny." in str(m.content) for m in messages if isinstance(m, AnyMessage))
