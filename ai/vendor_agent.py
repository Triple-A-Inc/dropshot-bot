import logging
from typing import List
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableConfig
from state import DropShotVendorGraphState
import os 
from langchain_openai import ChatOpenAI
from collections import deque

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DropShotVendorAI:
    def __init__(
        self,
        state: DropShotVendorGraphState,
        model: str,
        temperature: float,
        verbose: bool,
        tools: List = [],
    ):
        self.state = state
        self.model = model
        self.temperature = temperature
        self.verbose = verbose
        self.llm = ChatOpenAI(
            model=model,
            temperature=temperature,
            api_key=os.environ['OPENAI_API_KEY']
        )
        self.tools = tools

    def __call__(self, state: DropShotVendorGraphState, config: RunnableConfig):
        while True:
            result = self.runnable.invoke(state)
            if result.content and (not isinstance(result.content, list) or result.content[0].get("text")):
                break
            messages = state["messages"] + [("user", "Respond with a real output.")]
            state = {**state, "messages": messages}
        return {"messages": result}

    def get_llm(self):
        return self.llm

    def update_state(self, key, value):
        logger.info(f"Updating state: {key} -> {value}")
        self.state = {**self.state, key: value}

    def invoke(self, prompt: str):
        logger.info("DropShotVendorAI invoked")
        
        assistant_prompt = ChatPromptTemplate.from_messages([
            ("system", prompt),
            ("placeholder", "{messages}")
        ])
        llm = self.get_llm()
        if self.tools:
            chain = assistant_prompt | llm.bind_tools(self.tools)
        else:
            chain = assistant_prompt | llm  # Do not bind tools if none are provided
        self.runnable = chain
        
        return self.__call__(self.state, {"configurable": {"thread_id": '123'}})