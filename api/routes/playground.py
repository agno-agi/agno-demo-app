from os import getenv
from agno.playground import Playground

# Import agents
from agents.finance import get_finance_agent
from agents.research import get_research_agent
from agents.web_search import get_web_search_agent
from agents.basic import get_basic_agent
from agents.memory import get_memory_agent
from agents.reasoning import get_reasoning_agent

# Import workflows
from workflows.blog_post_generator import get_blog_post_generator
from workflows.investment_report_generator import get_investment_report_generator
from workflows.startup_idea_validator import get_startup_idea_validator

# Import teams
from teams.finance_researcher import get_finance_researcher_team
from teams.multi_language import get_multi_language_team

######################################################
## Router for the agent playground
######################################################

finance_agent = get_finance_agent(debug_mode=True)
research_agent = get_research_agent(debug_mode=True)
web_search_agent = get_web_search_agent(debug_mode=True)
basic_agent = get_basic_agent(debug_mode=True)
memory_agent = get_memory_agent(debug_mode=True)
reasoning_agent = get_reasoning_agent(debug_mode=True)

blog_post_generator = get_blog_post_generator(debug_mode=True)
investment_report_generator = get_investment_report_generator(debug_mode=True)
startup_idea_validator = get_startup_idea_validator(debug_mode=True)

finance_researcher_team = get_finance_researcher_team()
multi_language_team = get_multi_language_team()

# Create a playground instance
playground = Playground(
    agents=[basic_agent, web_search_agent, research_agent, finance_agent, memory_agent, reasoning_agent],
    workflows=[blog_post_generator, investment_report_generator, startup_idea_validator],
    teams=[finance_researcher_team, multi_language_team],
)
# Log the playground endpoint with app.agno.com
if getenv("RUNTIME_ENV") == "dev":
    playground.register_app_on_platform()

playground_router = playground.get_router()
