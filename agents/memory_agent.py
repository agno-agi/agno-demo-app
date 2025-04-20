from typing import Optional

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.storage.agent.postgres import PostgresAgentStorage
from agno.memory.v2.memory import Memory
from agno.memory.v2.db.postgres import PostgresMemoryDb

from agents.settings import agent_settings
from db.session import db_url


memory_agent_storage = PostgresAgentStorage(table_name="memory_agent", db_url=db_url, auto_upgrade_schema=True)
memory = Memory(db=PostgresMemoryDb(table_name="agent_memories", db_url=db_url))


def get_memory_agent(
    user_id: Optional[str] = None,
    session_id: Optional[str] = None,
    debug_mode: bool = False,
) -> Agent:
    return Agent(
        name="Memory Agent",
        role="Memory agent",
        agent_id="memory-agent",
        session_id=session_id,
        user_id=user_id,
        model=OpenAIChat(
            id=agent_settings.gpt_4o_mini,
            max_tokens=agent_settings.default_max_completion_tokens,
            temperature=agent_settings.default_temperature,
        ),
        memory=memory,
        enable_user_memories=True,
        storage=memory_agent_storage,
        add_history_to_messages=True,
        num_history_runs=5,
        add_datetime_to_instructions=True,
        markdown=True,
        debug_mode=debug_mode,
    )
