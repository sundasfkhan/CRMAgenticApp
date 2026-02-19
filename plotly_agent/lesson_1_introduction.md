# Lesson 1: Introduction to PlotlyVisualizationAgent

## Objective
In this lesson, students will learn about the purpose and functionality of the `PlotlyVisualizationAgent` class. They will understand how it uses the LangChain framework to create interactive data visualizations.

---

## Key Concepts

### What is `PlotlyVisualizationAgent`?
- A high-level wrapper for creating data visualizations using Plotly.
- Built on the LangChain framework, which enables conversational AI workflows.
- Designed to generate charts based on natural language instructions.

### Core Features
1. **Data Analysis**: Understands the structure of the input data.
2. **Chart Creation**: Generates interactive Plotly charts.
3. **Error Handling**: Repairs Plotly code if errors occur.
4. **Interactive Chat**: Allows users to interact with the agent in a conversational manner.

---

## Code Walkthrough

### Initialization
```python
agent = PlotlyVisualizationAgent(model="gpt-4o")
```
- `model`: Specifies the AI model (e.g., `gpt-4o`).
- `temperature`: Controls the randomness of responses (default is `0.0` for deterministic behavior).

### Creating a Chart
```python
result = agent.create_chart(
    data=my_dataframe,
    instruction="Create a pie chart showing CRM Cases Status distribution"
)
```
- `data`: The input data (e.g., a Pandas DataFrame).
- `instruction`: A natural language description of the desired chart.

### Interactive Session
```python
agent.interactive_session()
```
- Starts a chat session where users can give instructions and receive responses interactively.

---

## Activity
1. Initialize the `PlotlyVisualizationAgent` in your Python environment.
2. Create a simple bar chart using a sample DataFrame.
3. Explore the interactive session feature.

---

## Summary
The `PlotlyVisualizationAgent` is a powerful tool for creating data visualizations with minimal effort. It combines the capabilities of Plotly and LangChain to provide an intuitive and interactive experience.
