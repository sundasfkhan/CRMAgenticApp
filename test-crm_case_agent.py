import os
from dotenv import load_dotenv
from PowerPlatform.Dataverse.client import DataverseClient
from azure.identity import InteractiveBrowserCredential
from crm_case_agent import CRMCaseAgent

# Load environment variables from .env file
load_dotenv()

if __name__ == '__main__':

    # Get configuration from environment variables
    resource_url = os.getenv("DATAVERSE_RESOURCE_URL")

    # Show resource_url for debugging
    print(f"Using DATAVERSE_RESOURCE_URL={resource_url}")

    # Initialize credential and client (production Dataverse path)
    if not resource_url:
        raise ValueError("DATAVERSE_RESOURCE_URL environment variable is not set")

    # Use InteractiveBrowserCredential for user authentication
    print("Using InteractiveBrowserCredential() for authentication. A browser window may open for you to sign in...")
    credential = InteractiveBrowserCredential()

    # Trigger an interactive auth flow to prompt the user immediately (optional).
    # We use the Dataverse resource scope: '<resource_url>/.default'
    try:
        test_scope = f"{resource_url}/.default" if resource_url else None
        if test_scope:
            # This call will open a browser for interactive login if needed
            token = credential.get_token(test_scope)
            print(f"Obtained access token for scope: {test_scope} (expires_on={token.expires_on})")
    except Exception as e:
        print(f"Warning: Interactive auth failed or was not completed: {e}")

    client = DataverseClient(resource_url, credential)
    # Initialize the CRM Case Agent with the Dataverse client
    agent = CRMCaseAgent(dataverse_client=client)

    # Run a sample query (can be overridden with environment variable SAMPLE_QUERY)
    sample_query = os.getenv("SAMPLE_QUERY", "Get me all cases for customer Trey Research")

    try:
        print(f"Running sample query: {sample_query}")
        response = agent.run(sample_query)
        print("\nAgent response:\n")
        print(response)
    except Exception as e:
        print(f"Error running sample query: {e}")

    # Optionally start interactive session if INTERACTIVE env var is set
    interactive_flag = os.getenv("INTERACTIVE", "false").strip().lower()
    if interactive_flag in ("1", "true", "yes"):
        agent.chat()
