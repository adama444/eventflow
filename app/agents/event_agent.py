from pathlib import Path
from typing import TypedDict

import yaml
from langchain.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langgraph.graph import END, StateGraph

from app.core.config import settings
from app.core.logger import get_logger
from app.schemas.event_data import EventData

logger = get_logger(__name__)


def load_system_prompt() -> str:
    """Load system prompt from yaml file"""
    prompt_path = (
        Path(__file__).resolve().parent.parent / "prompts" / "event_prompt.yaml"
    )
    with open(prompt_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data["system_prompt"]


class ConversationState(TypedDict):
    """A simple conversation state for LangGraph."""

    messages: list


SYSTEM_PROMPT = load_system_prompt()

llm = ChatOllama(model=settings.ollama_model, temperature=0)

prompt_template = ChatPromptTemplate.from_messages(
    [("system", SYSTEM_PROMPT), ("human", "{input}")]
).partial(event_model=EventData().model_construct().model_dump_json())


def chatbot_node(state: ConversationState) -> ConversationState:
    """Main node: handles conversation turn."""
    user_message = state["messages"][-1]
    logger.info(f"User said: {user_message}")

    # Generate LLM response
    chain = prompt_template | llm
    ai_response = chain.invoke({"input": user_message})

    logger.info(f"AI response: {ai_response.content}")

    # Append AI response to messages
    state["messages"].append(ai_response.content)
    return state


# Build Graph
graph = StateGraph(ConversationState)
graph.add_node("chatbot", chatbot_node)
graph.set_entry_point("chatbot")
graph.add_edge("chatbot", END)

# Export Runnable App
chatbot_app = graph.compile()
