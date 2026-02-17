"""
Example usage of the Plotly Visualization Agent V2.

This file demonstrates how to use the latest LangChain agent framework
to create data visualizations with Plotly.
"""

from dotenv import load_dotenv
import pandas as pd

# Load environment variables
load_dotenv()

# Example 1: Using the high-level PlotlyVisualizationAgent class
def example_agent_class():
    """Demonstrate using the PlotlyVisualizationAgent class."""
    from plotly_agent_v2 import PlotlyVisualizationAgent

    # Create sample data
    data = pd.DataFrame({
        'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        'Sales': [1200, 1500, 1800, 2100, 1900, 2300],
        'Expenses': [800, 900, 1100, 1200, 1000, 1300],
        'Profit': [400, 600, 700, 900, 900, 1000]
    })

    # Initialize the agent
    agent = PlotlyVisualizationAgent(model="gpt-4o")

    # Create a chart
    result = agent.create_chart(
        data=data,
        instruction="Create a grouped bar chart showing Sales and Expenses by Month with a title"
    )

    if result["success"]:
        print("Chart created successfully!")
        print(result["response"])
    else:
        print(f"Error: {result['error']}")


# Example 2: Using the create_plotly_agent function directly
def example_create_agent():
    """Demonstrate using the create_plotly_agent function."""
    from plotly_agent_v2 import create_plotly_agent
    from langchain.messages import HumanMessage
    import json

    # Create sample data
    data = [
        {"Category": "A", "Value": 100},
        {"Category": "B", "Value": 250},
        {"Category": "C", "Value": 180},
        {"Category": "D", "Value": 320},
    ]

    # Create the agent
    agent = create_plotly_agent(model="gpt-4o")

    # Send a request
    response = agent.invoke({
        "messages": [
            HumanMessage(content=f"""
            Create a pie chart for this data: {json.dumps(data)}
            Show the percentage for each category.
            """)
        ]
    })

    print("Response:", response["messages"][-1].content)


# Example 3: Interactive chat session
def example_interactive():
    """Start an interactive session with the visualization agent."""
    from plotly_agent_v2 import PlotlyVisualizationAgent

    agent = PlotlyVisualizationAgent(model="gpt-4o")
    agent.interactive_session()


# Example 4: Quick chart creation
def example_quick_chart():
    """Demonstrate the quick_chart convenience function."""
    from plotly_agent_v2.agent import quick_chart

    data = {
        'Year': [2020, 2021, 2022, 2023, 2024],
        'Revenue': [1000000, 1200000, 1500000, 1800000, 2100000]
    }

    result = quick_chart(
        data=data,
        instruction="Create a line chart showing revenue growth over years with markers"
    )

    print("Result:", result)


if __name__ == "__main__":
    print("=" * 60)
    print("Plotly Visualization Agent V2 - Examples")
    print("=" * 60)

    # Uncomment the example you want to run:

    # example_agent_class()
    # example_create_agent()
    # example_interactive()
    example_quick_chart()

    print("\nUncomment one of the example functions to run it.")

