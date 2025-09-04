from pathlib import Path
from typing import Annotated, TypedDict

import psycopg
import yaml
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_ollama import ChatOllama
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.graph import END, StateGraph, add_messages
from psycopg.rows import dict_row

from app.core.config import settings
from app.core.logger import get_logger
from app.schemas.event import generate_sample_event

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

    messages: Annotated[list, add_messages]
    is_validated: bool


SYSTEM_PROMPT = load_system_prompt()

llm = ChatOllama(model=settings.ollama_model, temperature=0.5)

prompt_template = ChatPromptTemplate.from_messages(
    [("system", SYSTEM_PROMPT), MessagesPlaceholder("messages")]
).partial(event_model=generate_sample_event().model_dump_json())


def chatbot_node(state: ConversationState) -> ConversationState:
    """Main node: handles conversation turn."""
    chain = prompt_template | llm
    ai_response = chain.invoke({"messages": state["messages"]})

    state["messages"].append(ai_response)
    state["is_validated"] = True if "<<VALIDATED>>" in ai_response.content else False
    return state


# Build Graph
graph = StateGraph(ConversationState)
graph.add_node("chatbot", chatbot_node)
graph.set_entry_point("chatbot")  # Graph start
graph.add_edge("chatbot", END)

# Initialize PostgresSaver
conn = psycopg.connect(
    settings.psycopg_database_url,
    autocommit=True,
    row_factory=dict_row,
)
memory = PostgresSaver(conn)

# Export Runnable App
chatbot_app = graph.compile(checkpointer=memory)
