from typing import Annotated, TypedDict
from pydantic import BaseModel
from langgraph.graph.message import add_messages

class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"

class State(TypedDict):
    messages: Annotated[list, add_messages]
    session_id: str
