from typing import Optional
from textwrap import dedent

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.yfinance import YFinanceTools
from agno.storage.postgres import PostgresStorage

from agents.settings import agent_settings
from db.session import db_url


finance_agent_storage = PostgresStorage(table_name="finance_agent", db_url=db_url, auto_upgrade_schema=True)


def get_finance_agent(
    user_id: Optional[str] = None,
    session_id: Optional[str] = None,
    debug_mode: bool = False,
) -> Agent:
    return Agent(
        name="Finance Agent",
        role="Analyze financial data",
        agent_id="finance-agent",
        session_id=session_id,
        user_id=user_id,
        model=OpenAIChat(
            id=agent_settings.gpt_4,
            max_tokens=agent_settings.default_max_completion_tokens,
            temperature=agent_settings.default_temperature,
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
        storage=finance_agent_storage,
        add_history_to_messages=True,
        num_history_responses=5,
        add_datetime_to_instructions=True,
        markdown=True,
        debug_mode=debug_mode,
    )
