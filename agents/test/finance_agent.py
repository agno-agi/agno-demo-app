from agents.finance import get_finance_agent

finance_agent = get_finance_agent()

finance_agent.print_response("Tell me NVDA's stock price.", stream=True)
