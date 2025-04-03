from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.team.team import Team
from agno.storage.postgres import PostgresStorage
from db.session import db_url

japanese_agent = Agent(
    name="Japanese Agent",
    agent_id="japanese-agent",
    role="You only answer in Japanese",
    model=OpenAIChat(id="gpt-4o"),
)
chinese_agent = Agent(
    name="Chinese Agent",
    agent_id="chinese-agent",
    role="You only answer in Chinese",
    model=OpenAIChat(id="gpt-4o"),
)
spanish_agent = Agent(
    name="Spanish Agent",
    agent_id="spanish-agent",
    role="You only answer in Spanish",
    model=OpenAIChat(id="gpt-4o"),
)
french_agent = Agent(
    name="French Agent",
    agent_id="french-agent",
    role="You only answer in French",
    model=OpenAIChat(id="gpt-4o"),
)
german_agent = Agent(
    name="German Agent",
    agent_id="german-agent",
    role="You only answer in German",
    model=OpenAIChat(id="gpt-4o"),
)


def get_multi_language_team():
    return Team(
        name="Multi Language Team",
        mode="route",
        team_id="multi-language-team",
        model=OpenAIChat("gpt-4o"),
        members=[
            spanish_agent,
            japanese_agent,
            french_agent,
            german_agent,
            chinese_agent,
        ],
        description="You are a language router that directs questions to the appropriate language agent.",
        instructions=[
            "Identify the language of the user's question and direct it to the appropriate language agent.",
            "Let the language agent answer the question in the language of the user's question.",
            "The the user asks a question in English, respond directly in English with:",
            "If the user asks in a language that is not English or your don't have a member agent for that language, respond in English with:",
            "'I only answer in the following languages: English, Spanish, Japanese, Chinese, French and German. Please ask your question in one of these languages.'",
            "Always check the language of the user's input before routing to an agent.",
            "For unsupported languages like Italian, respond in English with the above message.",
        ],
        markdown=True,
        show_tool_calls=True,
        show_members_responses=True,
        storage=PostgresStorage(
            table_name="multi_language_team",
            db_url=db_url,
            mode="team",
            auto_upgrade_schema=True,
        ),
    )
