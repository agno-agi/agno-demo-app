from typing import Optional

from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.storage.postgres import PostgresStorage
from agno.tools.reasoning import ReasoningTools

from agents.settings import agent_settings
from db.session import db_url


reasoning_agent_storage = PostgresStorage(
    table_name="reasoning_agent", db_url=db_url, auto_upgrade_schema=True
)


def get_reasoning_agent(
    user_id: Optional[str] = None,
    session_id: Optional[str] = None,
    debug_mode: bool = False,
) -> Agent:
    return Agent(
        model=Claude(id=agent_settings.claude_4_sonnet),
        tools=[
            ReasoningTools(add_instructions=True),
        ],
        name="Reasoning Agent",
        role="Reasoning agent",
        agent_id="reasoning-agent",
        session_id=session_id,
        user_id=user_id,
        instructions="Use tables where possible",
        markdown=True,
        storage=reasoning_agent_storage,
        add_history_to_messages=True,
        num_history_responses=5,
        add_datetime_to_instructions=True,
        debug_mode=debug_mode,
    )
