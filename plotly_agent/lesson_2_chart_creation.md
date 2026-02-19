# Lesson 2: Chart Creation with PlotlyVisualizationAgent

## Objective
In this lesson, students will learn how to use the `create_chart` method to generate various types of charts based on natural language instructions.

---

## Key Concepts

### `create_chart` Method
- The primary method for generating charts.
- Accepts data and a natural language instruction as input.
- Returns a dictionary containing the chart or an error message.

### Workflow
1. Analyze the data structure.
2. Choose an appropriate chart type.
3. Generate the Plotly chart.
4. Handle errors and repair code if necessary.

---

## Code Walkthrough

### Example: Pie Chart
```python
crm_statuses = ['Open', 'In Progress', 'Resolved', 'Closed', 'Pending']
crm_counts = [random.randint(10, 100) for _ in range(len(crm_statuses))]

my_dataframe = pd.DataFrame({
    'Status': crm_statuses,
    'Count': crm_counts
})

result = agent.create_chart(
    data=my_dataframe,
    instruction="Create a pie chart showing CRM Cases Status distribution"
)

if result["success"]:
    print("Chart created successfully!")
    print(f"Response: {result['response']}")
else:
    print(f"Error: {result.get('error', 'Unknown error')}")
```

### Example: Bar Chart
```python
result = agent.create_chart(
    data=my_dataframe,
    instruction="Create a bar chart comparing CRM case statuses"
)
```

---

## Activity
1. Create a pie chart using the provided CRM data.
2. Modify the instruction to create a bar chart.
3. Experiment with different chart types (e.g., line chart, scatter plot).

---

## Summary
The `create_chart` method is versatile and easy to use. By providing clear instructions, students can generate a wide variety of charts to visualize their data.
