"""
Plotly Visualization Agent using Latest LangChain Agent Framework.

This module implements a data visualization agent using the latest
LangChain create_agent API with LangGraph backend.
"""

import os
import json
from typing import List, Optional, Dict, Any

from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.messages import HumanMessage, AIMessage

from .tools import create_plotly_chart, repair_plotly_code, get_dataframe_info


# System prompt for the visualization agent
VISUALIZATION_SYSTEM_PROMPT = """You are an expert data visualization assistant specializing in Plotly.

CAPABILITIES:
- Analyze data to determine the best chart type
- Create beautiful, interactive Plotly visualizations
- Handle errors and repair code when needed

WORKFLOW:
1. First, use get_dataframe_info to understand the data structure
2. Choose an appropriate chart type based on the data
3. Use create_plotly_chart to generate the visualization
4. If there's an error, use repair_plotly_code to fix it

CHART GUIDELINES:
- Always give charts a descriptive title using HTML bold tags: title="<b>My Title</b>"
- Format large numbers with appropriate suffixes (K, M, B)
- Add percentage signs and proper decimal places for percentages
- Format dates as Day/Month/Year when displayed
- Include hover information with useful details
- Use appropriate color schemes for the data type
- For line charts, include markers at data points
- For categorical comparisons, consider bar charts
- For trends over time, use line charts
- For distributions, use histograms or box plots
- For correlations, use scatter plots

CODE FORMAT:
Your plotly_code should always create a variable named 'fig'. Example:
```python
fig = px.bar(df, x='category', y='value', title='<b>My Chart</b>')
fig.update_layout(template='plotly_white')
```

When an error occurs, analyze the error message and fix the code accordingly."""


def create_plotly_agent(
    model: str = "gpt-4o",
    temperature: float = 0.0,
    verbose: bool = False
) -> Any:
    """
    Create a Plotly visualization agent using the latest LangChain framework.

    Args:
        model: The model name to use (e.g., "gpt-4o", "gpt-4.1", "gpt-4.1-mini")
        temperature: Temperature for model responses (0.0 for deterministic)
        verbose: Whether to enable verbose output

    Returns:
        A LangChain agent configured for Plotly visualization
    """
    # Initialize the chat model
    llm = init_chat_model(model, temperature=temperature)

    # Define the tools
    tools = [create_plotly_chart, repair_plotly_code, get_dataframe_info]

    # Create the agent using latest LangChain create_agent
    agent = create_agent(
        llm,
        tools=tools,
        system_prompt=VISUALIZATION_SYSTEM_PROMPT
    )

    return agent


class PlotlyVisualizationAgent:
    """
    High-level wrapper for the Plotly visualization agent.

    Provides a convenient interface for creating charts from data.
    """

    def __init__(
        self,
        model: str = "gpt-4o",
        temperature: float = 0.0,
        api_key: Optional[str] = None
    ):
        """
        Initialize the Plotly visualization agent.

        Args:
            model: The model name to use
            temperature: Temperature for model responses
            api_key: Optional OpenAI API key (can also be set via environment)
        """
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key

        self.model = model
        self.temperature = temperature
        self.agent = create_plotly_agent(model=model, temperature=temperature)
        self.chat_history: List = []

    def create_chart(
        self,
        data: Any,
        instruction: str,
        reset_history: bool = False
    ) -> Dict[str, Any]:
        """
        Create a chart based on data and natural language instruction.

        Args:
            data: DataFrame, dict, or list of dicts containing the data
            instruction: Natural language description of the desired chart
            reset_history: Whether to reset conversation history

        Returns:
            Dictionary containing the result (figure JSON or error)
        """
        import pandas as pd

        if reset_history:
            self.chat_history = []

        # Convert data to JSON
        if isinstance(data, pd.DataFrame):
            data_json = data.to_json(orient='records')
        elif isinstance(data, (list, dict)):
            data_json = json.dumps(data)
        else:
            data_json = str(data)

        # Construct the message
        user_message = f"""Please create a visualization for the following data:

DATA (JSON format):
{data_json}

INSTRUCTION:
{instruction}

First analyze the data structure, then create an appropriate chart."""

        # Build messages
        messages = list(self.chat_history)
        messages.append(HumanMessage(content=user_message))

        try:
            # Invoke the agent
            response = self.agent.invoke({"messages": messages})

            # Extract the response
            final_message = response["messages"][-1]
            response_content = final_message.content

            # Update history
            self.chat_history.append(HumanMessage(content=user_message))
            self.chat_history.append(AIMessage(content=response_content))

            return {
                "success": True,
                "response": response_content,
                "messages": response["messages"]
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def chat(self, message: str) -> str:
        """
        Send a chat message to the agent and get a response.

        Args:
            message: The user's message

        Returns:
            The agent's response as a string
        """
        messages = list(self.chat_history)
        messages.append(HumanMessage(content=message))

        try:
            response = self.agent.invoke({"messages": messages})
            response_content = response["messages"][-1].content

            # Update history
            self.chat_history.append(HumanMessage(content=message))
            self.chat_history.append(AIMessage(content=response_content))

            return response_content

        except Exception as e:
            return f"Error: {str(e)}"

    def interactive_session(self):
        """Start an interactive chat session with the visualization agent."""
        print("Plotly Visualization Agent Ready (LangChain v1)")
        print("Type 'exit' or 'quit' to end the session.")
        print("-" * 50)

        while True:
            try:
                user_input = input("\nYou: ").strip()
                if user_input.lower() in ['quit', 'exit']:
                    print("Goodbye!")
                    break

                if not user_input:
                    continue

                response = self.chat(user_input)
                print(f"\nAgent: {response}")

            except KeyboardInterrupt:
                print("\n\nSession interrupted. Goodbye!")
                break

    def reset(self):
        """Reset the conversation history."""
        self.chat_history = []


# Convenience function for quick chart creation
def quick_chart(data: Any, instruction: str, model: str = "gpt-4o") -> Dict[str, Any]:
    """
    Quickly create a chart without managing agent state.

    Args:
        data: The data to visualize
        instruction: Natural language description of desired chart
        model: The model to use

    Returns:
        Dictionary containing the result
    """
    agent = PlotlyVisualizationAgent(model=model)
    return agent.create_chart(data, instruction)

