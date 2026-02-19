import os
from typing import List, Optional
from dataclasses import dataclass

# Latest LangChain v1 Agent Imports
from langchain.agents import create_agent
from langchain.tools import tool, ToolRuntime
from langchain.messages import HumanMessage, AIMessage

# Utility imports
from utility_test import get_customer_cases, get_customer_name_from_case


# Define the context schema for dependency injection using dataclass
@dataclass
class CRMContext:
    dataverse_client: object


@tool
def retrieve_customer_cases(customer_name: str, runtime: ToolRuntime[CRMContext]) -> str:
    """
    Retrieves CRM cases for a specific customer by their name.
    Use this tool when the user asks about cases, incidents, or support tickets.

    Args:
        customer_name: The name of the customer to search for (e.g., "Trey Research", "John Smith")
    """
    # Access the dataverse client from runtime context
    dataverse_client = runtime.context.dataverse_client

    if dataverse_client is None:
        return "Error: Dataverse client not initialized."

    try:
        case_batches = get_customer_cases(dataverse_client, customer_name, top=10)

        cases_list = []
        for batch in case_batches:
            for case in batch:
                customer = get_customer_name_from_case(case)
                cases_list.append({
                    "customer": customer,
                    "title": case.get('title', 'N/A'),
                    "ticket_number": case.get('ticketnumber', 'N/A'),
                    "status": case.get('statuscode', 'N/A'),
                })

        if not cases_list:
            return f"No cases found for customer: {customer_name}"

        result = f"Found {len(cases_list)} case(s) for '{customer_name}':\n"
        for i, case in enumerate(cases_list, 1):
            result += f"{i}. {case['title']} (Ticket: {case['ticket_number']}) - Status: {case['status']}\n"
        return result

    except Exception as e:
        return f"Error retrieving cases: {str(e)}"


class CRMCaseAgent:
    """
    Latest LangChain v1 Agent implementation.
    """

    def __init__(self, dataverse_client, model: str = "gpt-4o", api_key: Optional[str] = None):
        # Store the dataverse client for context injection
        self.dataverse_client = dataverse_client

        # Set API key if provided
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key

        # Create the agent using the NEW LangChain v1 create_agent
        # Model can be specified as a string (e.g., "gpt-4o", "gpt-4.1")
        self.agent = create_agent(
            model,
            tools=[retrieve_customer_cases],
            context_schema=CRMContext,
            system_prompt="You are a CRM assistant. Use the provided tools to look up customer cases."
        )

    def run(self, query: str, chat_history: List = None) -> str:
        """Runs the agent and returns the string response."""
        messages = []
        if chat_history:
            messages.extend(chat_history)
        messages.append(HumanMessage(content=query))

        # Invoke the agent with context for dependency injection
        response = self.agent.invoke(
            {"messages": messages},
            context=CRMContext(dataverse_client=self.dataverse_client)
        )

        # Return the content of the final AI message
        return response["messages"][-1].content

    def chat(self):
        """Interactive session helper."""
        print("CRM Agent (LangChain v1) Ready. Type 'exit' to quit.")
        history: List = []

        while True:
            user_input = input("\nYou: ").strip()
            if user_input.lower() in ['quit', 'exit']:
                print("Goodbye!")
                break

            response_text = self.run(user_input, history)
            print(f"\nAgent: {response_text}")

            # Update history for context-aware follow-up questions
            history.append(HumanMessage(content=user_input))
            history.append(AIMessage(content=response_text))


# Usage Example:
# agent = CRMCaseAgent(my_dataverse_client)
# agent.chat()