from google.adk.agents import Agent
from google.adk.tools import google_search

root_agent = Agent(
    model='gemini-2.5-flash',
    name='google_search_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions and use tool google_search to answer user query.',
    tools=[google_search]
)
