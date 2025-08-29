from app.core.database import init_db
from app.schemas.user import User
from app.agents.agent import memory

print("Creating tables...")
init_db()
print("Tables created")
memory.setup()
print("LangGraph memory tables initialized")