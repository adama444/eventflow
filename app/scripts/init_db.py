import asyncio

from app.agents.agent import init_chatbot_app
from app.core.database import init_db
from app.schemas.user import User


async def main():
    print("Creating tables...")
    init_db()
    print("Tables created")

    chatbot_app = await init_chatbot_app()
    # This will initialize memory and setup its tables
    await chatbot_app.checkpointer.setup()
    print("LangGraph memory tables initialized")


asyncio.run(main())
