from langgraph.graph import StateGraph
from langgraph.graph import START, END
from langgraph.prebuilt import tools_condition
from langchain_core.messages import ToolMessage
from langchain_core.runnables import RunnableLambda
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from prompts import smart_vendor_prompt
from state import DropShotVendorGraphState
import logging
from vendor_agent import DropShotVendorAI
from typing import Literal
import os 
from collections import deque 
import json
from dotenv import load_dotenv
from tools import get_itens


load_dotenv()
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



def create_vendor(model, temperature, verbose):
    builder = StateGraph(DropShotVendorGraphState)

    builder.add_node("vendor",
        lambda state: DropShotVendorAI(
            state=state,
            model=model, 
            temperature=temperature,
            verbose=verbose,
            tools=[get_itens]
        ).invoke(
            prompt=smart_vendor_prompt
        )
    )

    builder.add_node("tools", create_tool_node_with_fallback([get_itens]))

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


def run_vendor_inference(graph, message, user_id):
    events = graph.stream(
        {"messages": [("user", message)]},
        config={
            
            "recursion_limit": 15,
            "configurable": {"thread_id": user_id}
        },
        stream_mode="values"
    )

    recent_event = deque(events, maxlen=1).pop()
    messages = recent_event.get('messages', [])
    last_message = messages[-1]
    response = last_message.content
    return response


vendor = create_vendor(model='gpt-4o-mini', temperature=1, verbose=True)

while True: 
    user_message = input('Insira a Mensagem aqui: ')
    response = run_vendor_inference(vendor, user_message, '123')

    print('*' * 100)
    print('HUMAN MESSAGE:')
    print(user_message)

    print('*' * 100)
    print('AI RESPONSE:')
    print(response)



