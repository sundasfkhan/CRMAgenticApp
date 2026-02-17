from dotenv import load_dotenv
load_dotenv()  # Load environment variables first

from plotly_agent_v2 import PlotlyVisualizationAgent
import pandas as pd
import random

if __name__ == '__main__':
    # Create sample dataframe with CRM Cases data
    crm_statuses = ['Open', 'In Progress', 'Resolved', 'Closed', 'Pending']
    crm_counts = [random.randint(10, 100) for _ in range(len(crm_statuses))]

    my_dataframe = pd.DataFrame({
        'Status': crm_statuses,
        'Count': crm_counts
    })

    agent = PlotlyVisualizationAgent(model="gpt-4o")

    print("Creating chart...")
    print(f"Data:\n{my_dataframe}\n")

    result = agent.create_chart(
        data=my_dataframe,
        instruction="Create a pie chart showing CRM Cases Status distribution"
    )

    if result["success"]:
        print("Chart created successfully!")
        print(f"Response: {result['response']}")
    else:
        print(f"Error: {result.get('error', 'Unknown error')}")

