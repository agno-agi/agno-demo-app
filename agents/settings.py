from pydantic_settings import BaseSettings


class AgentSettings(BaseSettings):
    """Agent settings that can be set using environment variables.

    Reference: https://pydantic-docs.helpmanual.io/usage/settings/
    """

    gpt_4: str = "gpt-4o"
    gpt_4o_mini: str = "gpt-4o-mini"
    embedding_model: str = "text-embedding-3-small"
    default_max_completion_tokens: int = 16000
    default_temperature: float = 0

    claude_3_7_sonnet: str = "claude-3-7-sonnet-latest"
    claude_4_sonnet: str = "claude-sonnet-4-20250514"


# Create an AgentSettings object
agent_settings = AgentSettings()
