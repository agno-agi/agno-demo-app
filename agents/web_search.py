from textwrap import dedent
from typing import Optional

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.serpapi import SerpApiTools
from agno.storage.postgres import PostgresStorage

from agents.settings import agent_settings
from db.session import db_url

web_search_agent_storage = PostgresStorage(
    table_name="web_search_agent", db_url=db_url, auto_upgrade_schema=True
)


def get_web_search_agent(
    user_id: Optional[str] = None,
    session_id: Optional[str] = None,
    debug_mode: bool = False,
) -> Agent:
    return Agent(
        name="Web Search Agent",
        role="Search the web for information",
        agent_id="web-search-agent",
        session_id=session_id,
        user_id=user_id,
        model=OpenAIChat(
            id=agent_settings.gpt_4,
            max_tokens=agent_settings.default_max_completion_tokens,
            temperature=agent_settings.default_temperature,
        ),
        tools=[SerpApiTools()],
        description="You are a Web Search Agent that has the special skill of searching the web for information and presenting the results in a structured manner.",
        instructions=[
            "To answer the user's question, first search the web for information by breaking down the user's question into smaller queries.",
            "Make sure you cover all the aspects of the question.",
            "Important: \n"
            " - Focus on legitimate sources\n"
            " - Always provide sources and the links to the information you used to answer the question\n"
            " - If you cannot find the answer, say so and ask the user to provide more details.",
            "Keep your answers concise and engaging.",
        ],
        expected_output=dedent("""\
        Your answer should be in the following format:

        {provide a detailed answer to the user's question}

        ### Sources
        {provide the sources and links to the information you used to answer the question}
        """),
        storage=web_search_agent_storage,
        add_history_to_messages=True,
        num_history_responses=5,
        add_datetime_to_instructions=True,
        markdown=True,
        debug_mode=debug_mode,
    )
