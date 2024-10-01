import logging
from typing import List, Optional
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableConfig
from state import DropShotVendorGraphState
from datetime import datetime
import os 
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv


load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

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
            if result.tool_calls or (result.content and not isinstance(result.content, list) or result.content[0].get("text")):
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
        logger.info("AppointmentAssistant invoked")
        
        appointment_assistant_prompt = ChatPromptTemplate.from_messages([
            ("system", prompt),
            ("placeholder", "{messages}")
        ])
        llm = self.get_llm()
        chain = appointment_assistant_prompt | llm.bind_tools(self.tools)
        self.runnable = chain
        
        return self.__call__(self.state, {"configurable": {"thread_id": '123'}})