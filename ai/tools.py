# Import things that are needed generically
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool, StructuredTool, tool


@tool
def get_itens(query: str) -> str:
    """Look up things online."""
    return "LangChain"