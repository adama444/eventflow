from pathlib import Path
from typing import Annotated, Any, TypedDict, cast

import psycopg
import yaml
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_ollama import ChatOllama
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.graph import END, StateGraph, add_messages
from psycopg.rows import dict_row

from app.core.config import settings
from app.schemas.event import Event


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


SYSTEM_PROMPT = load_system_prompt()

llm = ChatOllama(model=settings.ollama_model, temperature=0)

prompt_template = ChatPromptTemplate.from_messages(
    [("system", SYSTEM_PROMPT), MessagesPlaceholder("messages")]
).partial(event_model=Event().model_construct().model_dump_json())


def chatbot_node(state: ConversationState) -> ConversationState:
    """Main node: handles conversation turn."""
    chain = prompt_template | llm
    ai_response = chain.invoke({"messages": state["messages"]})

    # Append AI response to messages
    state["messages"].append(ai_response)

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
memory = PostgresSaver(cast(Any, conn))

# Export Runnable App
chatbot_app = graph.compile(checkpointer=memory)
