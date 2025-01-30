from typing import Optional

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.storage.agent.postgres import PostgresAgentStorage

from agents.settings import agent_settings
from db.session import db_url


simple_agent_storage = PostgresAgentStorage(table_name="simple_agent", db_url=db_url)


def get_simple_agent(
    user_id: Optional[str] = None,
    session_id: Optional[str] = None,
    debug_mode: bool = False,
) -> Agent:
    return Agent(
        name="Simple Agent",
        role="Simple agent",
        agent_id="simple-agent",
        session_id=session_id,
        user_id=user_id,
        model=OpenAIChat(
            id=agent_settings.gpt_4o_mini,
            max_tokens=agent_settings.default_max_completion_tokens,
            temperature=agent_settings.default_temperature,
        ),
        storage=simple_agent_storage,
        add_history_to_messages=True,
        num_history_responses=5,
        add_datetime_to_instructions=True,
        markdown=True,
        debug_mode=debug_mode,
    )
