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

    if not resource_url:
        raise ValueError("DATAVERSE_RESOURCE_URL environment variable is not set")

    credential = InteractiveBrowserCredential()
    client = DataverseClient(resource_url, credential)

    # Initialize the CRM Case Agent with the Dataverse client
    agent = CRMCaseAgent(dataverse_client=client)

    # Option 1: Run a single query
    # response = agent.run("Get me all cases for customer Trey Research")
    # print(response)

    # Option 2: Start an interactive chat session
    agent.chat()
