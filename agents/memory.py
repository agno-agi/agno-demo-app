from typing import Optional

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.storage.postgres import PostgresStorage
from agno.memory.v2.memory import Memory
from agno.memory.v2.db.postgres import PostgresMemoryDb

from agents.settings import agent_settings
from db.session import db_url


memory_agent_storage = PostgresStorage(
    table_name="memory_agent_storage", db_url=db_url, auto_upgrade_schema=True
)
memory_agent_db = PostgresMemoryDb(table_name="memory_agent_memory", db_url=db_url)


def get_memory_agent(
    user_id: Optional[str] = None,
    session_id: Optional[str] = None,
    debug_mode: bool = False,
) -> Agent:
    memory = Memory(db=memory_agent_db)

    return Agent(
        name="Memory Agent",
        role="Memory agent",
        agent_id="memory-agent",
        memory=memory,
        session_id=session_id,
        user_id=user_id,
        model=OpenAIChat(
            id=agent_settings.gpt_4o_mini,
            max_tokens=agent_settings.default_max_completion_tokens,
            temperature=agent_settings.default_temperature,
        ),
        storage=memory_agent_storage,
        add_history_to_messages=True,
        num_history_responses=5,
        add_datetime_to_instructions=True,
        markdown=True,
        enable_user_memories=True,
        debug_mode=debug_mode,
    )
