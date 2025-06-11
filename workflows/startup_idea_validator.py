import json
from typing import Iterator, Optional

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.storage.postgres import PostgresStorage
from agno.tools.googlesearch import GoogleSearchTools
from agno.utils.log import logger
from agno.workflow import RunResponse, Workflow, WorkflowCompletedEvent
from pydantic import BaseModel, Field

from workflows.settings import workflow_settings
from db.session import db_url


class IdeaClarification(BaseModel):
    originality: str = Field(..., description="Originality of the idea.")
    mission: str = Field(..., description="Mission of the company.")
    objectives: str = Field(..., description="Objectives of the company.")


class MarketResearch(BaseModel):
    total_addressable_market: str = Field(..., description="Total addressable market (TAM).")
    serviceable_available_market: str = Field(..., description="Serviceable available market (SAM).")
    serviceable_obtainable_market: str = Field(..., description="Serviceable obtainable market (SOM).")
    target_customer_segments: str = Field(..., description="Target customer segments.")


class StartupIdeaValidator(Workflow):
    idea_clarifier_agent: Agent = Agent(
        model=OpenAIChat(id=workflow_settings.gpt_4_mini),
        instructions=[
            "Given a user's startup idea, its your goal to refine that idea. ",
            "Evaluates the originality of the idea by comparing it with existing concepts. ",
            "Define the mission and objectives of the startup.",
        ],
        add_history_to_messages=True,
        add_datetime_to_instructions=True,
        response_model=IdeaClarification,
        structured_outputs=True,
        debug_mode=False,
    )

    market_research_agent: Agent = Agent(
        model=OpenAIChat(id=workflow_settings.gpt_4_mini),
        tools=[GoogleSearchTools()],
        instructions=[
            "You are provided with a startup idea and the company's mission and objectives. ",
            "Estimate the total addressable market (TAM), serviceable available market (SAM), and serviceable obtainable market (SOM). ",
            "Define target customer segments and their characteristics. ",
            "Search the web for resources if you need to.",
        ],
        add_history_to_messages=True,
        add_datetime_to_instructions=True,
        response_model=MarketResearch,
        structured_outputs=True,
        debug_mode=False,
    )

    competitor_analysis_agent: Agent = Agent(
        model=OpenAIChat(id=workflow_settings.gpt_4_mini),
        tools=[GoogleSearchTools()],
        instructions=[
            "You are provided with a startup idea and some market research related to the idea. ",
            "Identify existing competitors in the market. ",
            "Perform Strengths, Weaknesses, Opportunities, and Threats (SWOT) analysis for each competitor. ",
            "Assess the startup’s potential positioning relative to competitors.",
        ],
        add_history_to_messages=True,
        add_datetime_to_instructions=True,
        markdown=True,
        debug_mode=False,
    )

    report_agent: Agent = Agent(
        model=OpenAIChat(id=workflow_settings.gpt_4_mini),
        instructions=[
            "You are provided with a startup idea and other data about the idea. ",
            "Summarise everything into a single report.",
        ],
        add_history_to_messages=True,
        add_datetime_to_instructions=True,
        markdown=True,
        debug_mode=False,
    )

    def get_idea_clarification(self, startup_idea: str) -> Optional[IdeaClarification]:
        try:
            response: RunResponse = self.idea_clarifier_agent.run(startup_idea)

            # Check if we got a valid response
            if not response or not response.content:
                logger.warning("Empty Idea Clarification response")
            # Check if the response is of the expected type
            if not isinstance(response.content, IdeaClarification):
                logger.warning("Invalid response type")

            return response.content

        except Exception as e:
            logger.warning(f"Failed: {str(e)}")

        return None

    def get_market_research(
        self, startup_idea: str, idea_clarification: IdeaClarification
    ) -> Optional[MarketResearch]:
        agent_input = {"startup_idea": startup_idea, **idea_clarification.model_dump()}

        try:
            response: RunResponse = self.market_research_agent.run(json.dumps(agent_input, indent=4))

            # Check if we got a valid response
            if not response or not response.content:
                logger.warning("Empty Market Research response")

            # Check if the response is of the expected type
            if not isinstance(response.content, MarketResearch):
                logger.warning("Invalid response type")

            return response.content

        except Exception as e:
            logger.warning(f"Failed: {str(e)}")

        return None

    def get_competitor_analysis(self, startup_idea: str, market_research: MarketResearch) -> Optional[str]:
        agent_input = {"startup_idea": startup_idea, **market_research.model_dump()}

        try:
            response: RunResponse = self.competitor_analysis_agent.run(json.dumps(agent_input, indent=4))

            # Check if we got a valid response
            if not response or not response.content:
                logger.warning("Empty Competitor Analysis response")

            return response.content

        except Exception as e:
            logger.warning(f"Failed: {str(e)}")

        return None

    def run(self, startup_idea: str) -> Iterator[WorkflowCompletedEvent]:  # type: ignore
        logger.info(f"Generating a startup validation report for: {startup_idea}")

        if self.run_id is None:
            raise ValueError("Run ID is not set")

        # Clarify and quantify the idea
        idea_clarification: Optional[IdeaClarification] = self.get_idea_clarification(startup_idea)

        if idea_clarification is None:
            yield WorkflowCompletedEvent(
                run_id=self.run_id,
                content=f"Sorry, could not even clarify the idea: {startup_idea}",
            )
            return

        # Do some market research
        market_research: Optional[MarketResearch] = self.get_market_research(startup_idea, idea_clarification)

        if market_research is None:
            yield WorkflowCompletedEvent(
                run_id=self.run_id,
                content="Market research failed",
            )
            return

        competitor_analysis: Optional[str] = self.get_competitor_analysis(startup_idea, market_research)

        # Compile the final report
        final_response: RunResponse = self.report_agent.run(
            json.dumps(
                {
                    "startup_idea": startup_idea,
                    **idea_clarification.model_dump(),
                    **market_research.model_dump(),
                    "competitor_analysis_report": competitor_analysis,
                },
                indent=4,
            )
        )

        yield WorkflowCompletedEvent(
            run_id=self.run_id,
            content=final_response.content,
        )


def get_startup_idea_validator(debug_mode: bool = False) -> StartupIdeaValidator:
    return StartupIdeaValidator(
        workflow_id="validate-startup-idea",
        storage=PostgresStorage(
            table_name="startup_idea_validator_workflows",
            db_url=db_url,
            mode="workflow",
            auto_upgrade_schema=True,
        ),
        debug_mode=debug_mode,
    )
