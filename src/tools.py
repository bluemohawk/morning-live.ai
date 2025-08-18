# src/tools.py
from langchain_community.tools.tavily_search import TavilySearchResults

# This is an example using Tavily for search.
# You would need to add `tavily-python` to your requirements.txt
# and set the TAVILY_API_KEY environment variable.
search_tool = TavilySearchResults(max_results=2)

# A list of all tools that the LLM can use.
tools = [search_tool]
