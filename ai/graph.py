from langbuilder.builder import StateGraph
from langbuilder.builder import START, END
from langbuilder.prebuilt import tools_condition
from langchain_core.messages import ToolMessage
from langchain_core.runnables import RunnableLambda
from langbuilder.prebuilt import ToolNode
from langbuilder.checkpoint.memory import MemorySaver
from prompts import smart_vendor_prompt
from state import DropShotVendorGraphState
import logging
from vendor_agent import DropShotVendorAI
from typing import Literal
import os 

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def handle_tool_error(state) -> dict:
    error = state.get("error")
    tool_calls = state["messages"][-1].tool_calls
    
    return {
        "messages": [
            ToolMessage(
                content=f"Error: {repr(error)}\n please fix your mistakes.",
                tool_call_id=tc["id"],
            )
            for tc in tool_calls
        ]
    }

def create_tool_node_with_fallback(tools: list) -> dict:
    return ToolNode(tools).with_fallbacks(
        [RunnableLambda(handle_tool_error)], exception_key="error"
    )

def print_event(event: dict, printed: set, max_length=1500):
    current_state = event.get("dialog_state")
    if current_state:
        print("Currently in: ", current_state[-1], flush=True)
    message = event.get("messages")
    if message:
        if isinstance(message, list):
            message = message[-1]
        if message.id not in printed:
            msg_repr = message.pretty_repr(html=True)
            if len(msg_repr) > max_length:
                msg_repr = msg_repr[:max_length] + " ... (truncated)"
            print(msg_repr, flush=True)
            printed.add(message.id)



def route_vendor(
        state: DropShotVendorGraphState
) -> Literal[
    "tools",
    "__end__"
]:
    if tools_condition(state) == END:
        return END

    if state["messages"][-1].tool_calls:
        return "tools"



def create_appointment_graph(model, temperature, verbose):
    builder = StateGraph(DropShotVendorGraphState)

    builder.add_node("vendor",
        lambda state: DropShotVendorAI(
            state=state,
            model=model, 
            temperature=temperature,
            verbose=verbose
        ).invoke(
            prompt=smart_vendor_prompt
        )
    )

    builder.add_node("tools", create_tool_node_with_fallback())

    builder.add_edge(START, "vendor")
    builder.add_edge("tools", "vendor")

    builder.add_conditional_edges(
        "vendor",
        route_vendor,
            {
                "tools": "tools",
                END: END,
            }
    )

    memory = MemorySaver()
    graph = builder.compile(
        checkpointer=memory,

    )

    return graph


