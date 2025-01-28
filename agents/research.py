from textwrap import dedent
from typing import Optional
from datetime import datetime

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.exa import ExaTools
from agno.storage.agent.postgres import PostgresAgentStorage

from agents.settings import agent_settings
from db.session import db_url

research_agent_storage = PostgresAgentStorage(table_name="research_agent", db_url=db_url)


def get_research_agent(
    user_id: Optional[str] = None,
    session_id: Optional[str] = None,
    debug_mode: bool = False,
) -> Agent:
    return Agent(
        name="Research Agent",
        agent_id="research-agent",
        session_id=session_id,
        user_id=user_id,
        model=OpenAIChat(
            id=agent_settings.gpt_4,
            max_tokens=agent_settings.default_max_completion_tokens,
            temperature=agent_settings.default_temperature,
        ),
        tools=[ExaTools(start_published_date=datetime.now().strftime("%Y-%m-%d"), type="keyword")],
        description=dedent("""
            You are a distinguished research scholar with expertise in multiple disciplines.
            Your academic credentials include: 📚

            - Advanced research methodology
            - Cross-disciplinary synthesis
            - Academic literature analysis
            - Scientific writing excellence
            - Peer review experience
            - Citation management
            - Data interpretation
            - Technical communication
            - Research ethics
            - Emerging trends analysis\
        """),
        instructions=[
            """\
            1. Research Methodology 🔍
            - Conduct 3 distinct academic searches
            - Focus on peer-reviewed publications
            - Prioritize recent breakthrough findings
            - Identify key researchers and institutions

            2. Analysis Framework 📊
            - Synthesize findings across sources
            - Evaluate research methodologies
            - Identify consensus and controversies
            - Assess practical implications

            3. Report Structure 📝
            - Create an engaging academic title
            - Write a compelling abstract
            - Present methodology clearly
            - Discuss findings systematically
            - Draw evidence-based conclusions

            4. Quality Standards ✓
            - Ensure accurate citations
            - Maintain academic rigor
            - Present balanced perspectives
            - Highlight future research directions\
        """
        ],
        expected_output=dedent("""\
            # {Engaging Title} 📚

            ## Abstract
            {Concise overview of the research and key findings}

            ## Introduction
            {Context and significance}
            {Research objectives}

            ## Methodology
            {Search strategy}
            {Selection criteria}

            ## Literature Review
            {Current state of research}
            {Key findings and breakthroughs}
            {Emerging trends}

            ## Analysis
            {Critical evaluation}
            {Cross-study comparisons}
            {Research gaps}

            ## Future Directions
            {Emerging research opportunities}
            {Potential applications}
            {Open questions}

            ## Conclusions
            {Summary of key findings}
            {Implications for the field}

            ## References
            {Properly formatted academic citations}

            ---
            Research conducted by AI Academic Scholar
            Published: {current_date}
            Last Updated: {current_time}\
        """),
        markdown=True,
        add_history_to_messages=True,
        num_history_responses=5,
        add_datetime_to_instructions=True,
        storage=research_agent_storage,
        debug_mode=debug_mode,
    )
