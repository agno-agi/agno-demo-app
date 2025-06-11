from textwrap import dedent
from typing import Iterator, Union

from agno.agent import Agent, RunResponse, RunResponseEvent
from agno.models.openai import OpenAIChat
from agno.storage.postgres import PostgresStorage
from agno.tools.yfinance import YFinanceTools
from agno.utils.log import logger
from agno.workflow import Workflow, WorkflowCompletedEvent

from workflows.settings import workflow_settings
from db.session import db_url


class InvestmentReportGenerator(Workflow):
    """Advanced workflow for generating professional investment analysis with strategic recommendations."""

    description: str = dedent("""\
    An intelligent investment analysis system that produces comprehensive financial research and
    strategic investment recommendations. This workflow orchestrates multiple AI agents to analyze
    market data, evaluate investment potential, and create detailed portfolio allocation strategies.
    The system excels at combining quantitative analysis with qualitative insights to deliver
    actionable investment advice.
    """)

    stock_analyst: Agent = Agent(
        name="Stock Analyst",
        model=OpenAIChat(id=workflow_settings.gpt_4_mini),
        tools=[YFinanceTools(company_info=True, analyst_recommendations=True, company_news=True)],
        description=dedent("""\
        You are MarketMaster-X, an elite Senior Investment Analyst at Goldman Sachs with expertise in:

        - Comprehensive market analysis
        - Financial statement evaluation
        - Industry trend identification
        - News impact assessment
        - Risk factor analysis
        - Growth potential evaluation\
        """),
        instructions=dedent("""\
        1. Market Research 📊
           - Analyze company fundamentals and metrics
           - Review recent market performance
           - Evaluate competitive positioning
           - Assess industry trends and dynamics
        2. Financial Analysis 💹
           - Examine key financial ratios
           - Review analyst recommendations
           - Analyze recent news impact
           - Identify growth catalysts
        3. Risk Assessment 🎯
           - Evaluate market risks
           - Assess company-specific challenges
           - Consider macroeconomic factors
           - Identify potential red flags
        Note: This analysis is for educational purposes only.\
        """),
        expected_output="Comprehensive market analysis report in markdown format",
    )

    research_analyst: Agent = Agent(
        name="Research Analyst",
        model=OpenAIChat(id=workflow_settings.gpt_4_mini),
        description=dedent("""\
        You are ValuePro-X, an elite Senior Research Analyst at Goldman Sachs specializing in:

        - Investment opportunity evaluation
        - Comparative analysis
        - Risk-reward assessment
        - Growth potential ranking
        - Strategic recommendations\
        """),
        instructions=dedent("""\
        1. Investment Analysis 🔍
           - Evaluate each company's potential
           - Compare relative valuations
           - Assess competitive advantages
           - Consider market positioning
        2. Risk Evaluation 📈
           - Analyze risk factors
           - Consider market conditions
           - Evaluate growth sustainability
           - Assess management capability
        3. Company Ranking 🏆
           - Rank based on investment potential
           - Provide detailed rationale
           - Consider risk-adjusted returns
           - Explain competitive advantages\
        """),
        expected_output="Detailed investment analysis and ranking report in markdown format",
    )

    investment_lead: Agent = Agent(
        name="Investment Lead",
        model=OpenAIChat(id=workflow_settings.gpt_4_mini),
        description=dedent("""\
        You are PortfolioSage-X, a distinguished Senior Investment Lead at Goldman Sachs expert in:

        - Portfolio strategy development
        - Asset allocation optimization
        - Risk management
        - Investment rationale articulation
        - Client recommendation delivery\
        """),
        instructions=dedent("""\
        1. Portfolio Strategy 💼
           - Develop allocation strategy
           - Optimize risk-reward balance
           - Consider diversification
           - Set investment timeframes
        2. Investment Rationale 📝
           - Explain allocation decisions
           - Support with analysis
           - Address potential concerns
           - Highlight growth catalysts
        3. Recommendation Delivery 📊
           - Present clear allocations
           - Explain investment thesis
           - Provide actionable insights
           - Include risk considerations\
        """),
    )

    def run(self, companies: str) -> Iterator[Union[WorkflowCompletedEvent, RunResponseEvent]]:  # type: ignore
        logger.info(f"Getting investment reports for companies: {companies}")

        if self.run_id is None:
            raise ValueError("Run ID is not set")

        initial_report: RunResponse = self.stock_analyst.run(companies)
        if initial_report is None or not initial_report.content:
            yield WorkflowCompletedEvent(
                run_id=self.run_id,
                content="Sorry, could not get the stock analyst report.",
            )
            return

        logger.info("Ranking companies based on investment potential.")
        ranked_companies: RunResponse = self.research_analyst.run(initial_report.content)
        if ranked_companies is None or not ranked_companies.content:
            yield WorkflowCompletedEvent(
                run_id=self.run_id,
                content="Sorry, could not get the ranked companies.",
            )
            return

        logger.info("Reviewing the research report and producing an investment proposal.")
        yield from self.investment_lead.run(ranked_companies.content, stream=True)


def get_investment_report_generator(debug_mode: bool = False) -> InvestmentReportGenerator:
    return InvestmentReportGenerator(
        workflow_id="generate-investment-report",
        storage=PostgresStorage(
            table_name="investment_report_generator_workflows",
            db_url=db_url,
            mode="workflow",
            auto_upgrade_schema=True,
        ),
        debug_mode=debug_mode,
    )
