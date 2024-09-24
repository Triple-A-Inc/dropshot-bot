from typing import TypedDict, Annotated, Literal, Optional
from langgraph.graph.message import AnyMessage, add_messages

class DropShotVendorGraphState(TypedDict):
    thread_id: str
    messages: Annotated[list[AnyMessage], add_messages]

state = {
    "thread_id": "",
    "messages": [],
}