from os import getenv
from agno.playground import Playground

# Import agents
from agents.finance import get_finance_agent
from agents.research import get_research_agent
from agents.web_search import get_web_search_agent

# Import workflows
from workflows.blog_post_generator import BlogPostGenerator
from workflows.investment_report_generator import InvestmentReportGenerator
from workflows.startup_idea_validator import StartupIdeaValidator

######################################################
## Router for the agent playground
######################################################

finance_agent = get_finance_agent(debug_mode=True)
research_agent = get_research_agent(debug_mode=True)
web_search_agent = get_web_search_agent(debug_mode=True)

blog_post_generator = BlogPostGenerator(workflow_id="blog_post_generator", debug_mode=True)
investment_report_generator = InvestmentReportGenerator(workflow_id="investment_report_generator", debug_mode=True)
startup_idea_validator = StartupIdeaValidator(workflow_id="startup_idea_validator", debug_mode=True)

# Create a playground instance
playground = Playground(
    agents=[web_search_agent, research_agent, finance_agent],
    workflows=[blog_post_generator, investment_report_generator, startup_idea_validator],
)
# Log the playground endpoint with phidata.app
if getenv("RUNTIME_ENV") == "dev":
    playground.create_endpoint("http://localhost:8000")

playground_router = playground.get_router()
