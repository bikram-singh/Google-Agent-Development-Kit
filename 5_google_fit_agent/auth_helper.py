import os
import json
import pathlib
from dotenv import load_dotenv
from google_auth_oauthlib.flow import InstalledAppFlow

# Load environment variables from .env file
load_dotenv()

# We will create a temporary secrets file for the library to use
CLIENT_SECRETS_FILE = "client_secrets.json"
SCOPES = os.getenv("SCOPES", "").split()

# Create the client_secrets.json structure from your .env file
client_config = {
    "installed": {
        "client_id": os.getenv("CLIENT_ID"),
        "client_secret": os.getenv("CLIENT_SECRET"),
        "redirect_uris": [os.getenv("REDIRECT_URI")],
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token"
    }
}
with open(CLIENT_SECRETS_FILE, "w") as f:
    json.dump(client_config, f)

# Use the standard library function to create a flow from the file
flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES)

# Use the console flow - it's much easier than running a local server.
# It will print a URL, you paste it in your browser, and paste the code back.
creds = flow.run_local_server(port=8090)

# Save the credentials to "token.json" (no dot at the beginning)
token_path = pathlib.Path("token.json")
with open(token_path, "w") as token_file:
    token_file.write(creds.to_json())

print(f"\n✅ Credentials successfully saved to {token_path}")

# Clean up the temporary secrets file
os.remove(CLIENT_SECRETS_FILE)