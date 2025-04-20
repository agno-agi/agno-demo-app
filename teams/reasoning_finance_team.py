from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.team.team import Team
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.reasoning import ReasoningTools
from agno.tools.yfinance import YFinanceTools

web_agent = Agent(
    name="Web Search Agent",
    role="Handle web search requests",
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=[DuckDuckGoTools()],
    instructions="Always include sources",
    add_datetime_to_instructions=True,
)

finance_agent = Agent(
    name="Finance Agent",
    role="Handle financial data requests",
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, company_info=True)],
    instructions=[
        "You are a financial data specialist. Provide concise and accurate data.",
        "Use tables to display stock prices, fundamentals (P/E, Market Cap), and recommendations.",
        "Clearly state the company name and ticker symbol.",
        "Briefly summarize recent company-specific news if available.",
        "Focus on delivering the requested financial data points clearly.",
    ],
    add_datetime_to_instructions=True,
)


def get_reasoning_finance_team():
    return Team(
        name="Reasoning Finance Team",
        mode="coordinate",
        model=OpenAIChat(id="gpt-4o"),
        members=[
            web_agent,
            finance_agent,
        ],
        tools=[ReasoningTools(add_instructions=True)],
        instructions=[
            "Only output the final answer, no other text.",
            "Use tables to display data",
        ],
        markdown=True,
        show_members_responses=True,
        enable_agentic_context=True,
        add_datetime_to_instructions=True,
        success_criteria="The team has successfully completed the task.",
    )
