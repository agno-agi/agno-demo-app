from agno.agent import Agent
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.models.openai import OpenAIChat
from agno.storage.postgres import PostgresStorage
from db.session import db_url
from agents.finance import get_finance_agent
from agno.team.team import Team

web_agent = Agent(
    name="Web Agent",
    role="Search the web for information",
    model=OpenAIChat(id="gpt-4o"),
    tools=[DuckDuckGoTools(cache_results=True)],
    agent_id="web-agent",
    instructions=[
        "You are an experienced web researcher and news analyst!",
    ],
    show_tool_calls=True,
    markdown=True,
    storage=PostgresStorage(table_name="web_agent", db_url=db_url, auto_upgrade_schema=True),
)

finance_agent = get_finance_agent(debug_mode=True)


def get_finance_researcher_team():
    return Team(
        name="Finance Researcher Team",
        team_id="financial-researcher-team",
        mode="route",
        members=[web_agent, finance_agent],
        instructions=[
            "You are a team of finance researchers!",
        ],
        description="You are a team of finance researchers!",
        model=OpenAIChat(id="gpt-4o"),
        success_criteria="A good financial research report.",
        enable_agentic_context=True,
        expected_output="A good financial research report.",
        storage=PostgresStorage(
            table_name="finance_researcher_team",
            db_url=db_url,
            mode="team",
            auto_upgrade_schema=True,
        ),
    )
