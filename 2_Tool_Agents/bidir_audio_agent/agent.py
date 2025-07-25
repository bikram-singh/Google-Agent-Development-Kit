from google.adk.agents import Agent
from google.adk.tools import google_search

root_agent = Agent(
    name="bidir_audio_agent",
    model="gemini-2.0-flash-live-001", 
    description="Bi-directional Audio agent that can use Google Search",
    instruction="""You are a helpful assistant. If you need to find recent
    or specific information, use the google_search tool.""",

    tools=[google_search],
)
