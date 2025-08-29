from typing import Any, cast
from app.agents.agent import chatbot_app

state = {"messages": ["Hello, I want to register a new event."]}
result = chatbot_app.invoke(cast(Any, state))
print(result["messages"])
