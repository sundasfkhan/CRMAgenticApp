import os
from typing import List, Optional
from langchain.agents import create_agent
from langchain.messages import HumanMessage, AIMessage
from .tools import retrieve_customer_cases, CRMContext


class CRMCaseAgent:
    def __init__(self, dataverse_client, model: str = "gpt-4o", api_key: Optional[str] = None):
        self.dataverse_client = dataverse_client
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key

        self.agent = create_agent(
            model,
            tools=[retrieve_customer_cases],
            context_schema=CRMContext,
            system_prompt="You are a CRM assistant. Use the provided tools to look up customer cases."
        )

    def run(self, query: str, chat_history: List = None) -> str:
        messages = []
        if chat_history:
            messages.extend(chat_history)
        messages.append(HumanMessage(content=query))

        response = self.agent.invoke(
            {"messages": messages},
            context=CRMContext(dataverse_client=self.dataverse_client)
        )

        return response["messages"][-1].content

    def chat(self):
        print("CRM Agent (LangChain v1) Ready. Type 'exit' to quit.")
        history: List = []
        while True:
            user_input = input("\nYou: ").strip()
            if user_input.lower() in ['quit', 'exit']:
                print("Goodbye!")
                break

            response_text = self.run(user_input, history)
            print(f"\nAgent: {response_text}")

            history.append(HumanMessage(content=user_input))
            history.append(AIMessage(content=response_text))

