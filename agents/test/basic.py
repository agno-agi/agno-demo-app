from agno.agent import Agent
from agno.models.openai import OpenAIChat

agent = Agent(model=OpenAIChat(id="gpt-4o"), markdown=True)

# Print the response in the terminal
agent.print_response("Share a 2 sentence horror story")
