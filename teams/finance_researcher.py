from textwrap import dedent
from typing import Optional

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.storage.postgres import PostgresStorage
from agno.team.team import Team
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools

from db.session import db_url
from teams.settings import team_settings

finance_agent = Agent(
    name="Finance Agent",
    role="Analyze financial data",
    agent_id="finance-agent",
    model=OpenAIChat(
        id=team_settings.gpt_4,
        max_tokens=team_settings.default_max_completion_tokens,
        temperature=team_settings.default_temperature,
    ),
    tools=[YFinanceTools(enable_all=True, cache_results=True)],
    instructions=dedent("""\
        You are a seasoned Wall Street analyst with deep expertise in market analysis! 📊

        Follow these steps for comprehensive financial analysis:
        1. Market Overview
        - Latest stock price
        - 52-week high and low
        2. Financial Deep Dive
        - Key metrics (P/E, Market Cap, EPS)
        3. Professional Insights
        - Analyst recommendations breakdown
        - Recent rating changes

        4. Market Context
        - Industry trends and positioning
        - Competitive analysis
        - Market sentiment indicators

        Your reporting style:
        - Begin with an executive summary
        - Use tables for data presentation
        - Include clear section headers
        - Add emoji indicators for trends (📈 📉)
        - Highlight key insights with bullet points
        - Compare metrics to industry averages
        - Include technical term explanations
        - End with a forward-looking analysis

        Risk Disclosure:
        - Always highlight potential risk factors
        - Note market uncertainties
        - Mention relevant regulatory concerns
    """),
    storage=PostgresStorage(table_name="finance_agent", db_url=db_url, auto_upgrade_schema=True),
    add_history_to_messages=True,
    num_history_responses=5,
    add_datetime_to_instructions=True,
    markdown=True,
)

web_agent = Agent(
    name="Web Agent",
    role="Search the web for information",
    model=OpenAIChat(
        id=team_settings.gpt_4,
        max_tokens=team_settings.default_max_completion_tokens,
        temperature=team_settings.default_temperature,
    ),
    tools=[DuckDuckGoTools(cache_results=True)],
    agent_id="web-agent",
    instructions=[
        "You are an experienced web researcher and news analyst!",
    ],
    show_tool_calls=True,
    markdown=True,
    storage=PostgresStorage(table_name="web_agent", db_url=db_url, auto_upgrade_schema=True),
)


def get_finance_researcher_team(
    model_id: Optional[str] = None,
    user_id: Optional[str] = None,
    session_id: Optional[str] = None,
    debug_mode: bool = True,
):
    model_id = model_id or team_settings.gpt_4

    return Team(
        name="Finance Researcher Team",
        team_id="financial-researcher-team",
        mode="route",
        members=[web_agent, finance_agent],
        instructions=[
            "You are a team of finance researchers!",
        ],
        session_id=session_id,
        user_id=user_id,
        description="You are a team of finance researchers!",
        model=OpenAIChat(
            id=model_id,
            max_tokens=team_settings.default_max_completion_tokens,
            temperature=team_settings.default_temperature,
        ),
        success_criteria="A good financial research report.",
        enable_agentic_context=True,
        expected_output="A good financial research report.",
        storage=PostgresStorage(
            table_name="finance_researcher_team",
            db_url=db_url,
            mode="team",
            auto_upgrade_schema=True,
        ),
        debug_mode=debug_mode,
    )
