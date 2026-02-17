from dotenv import load_dotenv
load_dotenv()  # Load environment variables first

from plotly_agent_v2 import PlotlyVisualizationAgent
import pandas as pd
import random

if __name__ == '__main__':
    # Create sample dataframe with random sales data
    my_dataframe = pd.DataFrame({
        'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        'Sales': [random.randint(5000, 20000) for _ in range(12)]
    })

    agent = PlotlyVisualizationAgent(model="gpt-4o")

    print("Creating chart...")
    print(f"Data:\n{my_dataframe}\n")

    result = agent.create_chart(
        data=my_dataframe,
        instruction="Create a bar chart showing sales by month"
    )

    if result["success"]:
        print("Chart created successfully!")
        print(f"Response: {result['response']}")
    else:
        print(f"Error: {result.get('error', 'Unknown error')}")

