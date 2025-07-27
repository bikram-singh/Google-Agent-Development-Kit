import os
import json
import requests
from google.adk.agents import Agent
from dotenv import load_dotenv


load_dotenv()


def get_access_token() -> str | None:
    """Reads the access token from the token.json file."""
    try:
        
        with open("5_google_fit_agent/token.json", "r") as f:
            creds = json.load(f)
        return creds.get("token")
    except FileNotFoundError:
        print("Error: 5_google_fit_agent/token.json not found. Please run auth_helper.py from inside the agent directory first.")
        return None
    except (KeyError, json.JSONDecodeError):
        print("Error: Invalid token.json file.")
        return None

# 1. Define your tool as a plain Python function.
#    The docstring is VERY important, as it becomes the tool's description.
def fetch_google_fit_steps(inputs: dict) -> dict:
    """
    Fetches aggregated daily step count data from Google Fit for a given time range.
    The 'inputs' dictionary must contain 'startTimeMillis' and 'endTimeMillis'.
    """
    access_token = get_access_token()
    if not access_token:
        return {"error": "Could not retrieve access token. Run authentication first."}

    start_time = inputs.get("startTimeMillis")
    end_time = inputs.get("endTimeMillis")

    if not start_time or not end_time:
        return {"error": "Missing 'startTimeMillis' or 'endTimeMillis' in inputs."}

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    body = {
        "aggregateBy": [{
            "dataTypeName": "com.google.step_count.delta",
            "dataSourceId": "derived:com.google.step_count.delta:com.google.android.gms:estimated_steps"
        }],
        "bucketByTime": { "durationMillis": 86400000 },
        "startTimeMillis": start_time,
        "endTimeMillis": end_time
    }
    response = requests.post(
        "https://www.googleapis.com/fitness/v1/users/me/dataset:aggregate",
        headers=headers,
        data=json.dumps(body)
    )
    if response.status_code != 200:
        return {"error": f"API request failed with status {response.status_code}", "details": response.text}

    return {"steps_data": response.json()}


# 2. Create the Agent, telling it which model to use.
agent = Agent(
    name="google_fit_agent",
    description="An agent to interact with the Google Fit API.",
    model="gemini-1.5-pro-latest",  
    tools=[fetch_google_fit_steps],
)