from agents.research import get_research_agent

research_agent = get_research_agent()

research_agent.print_response("Tell me about simulation theory", stream=True)
