# Lesson 4: Internal Functionality of PlotlyVisualizationAgent

## Objective
In this lesson, students will explore the internal functionality of the `PlotlyVisualizationAgent` class. They will learn how the agent is structured and how its components interact to create visualizations.

---

## Key Concepts

### Internal Components
1. **System Prompt**: Defines the agent's capabilities and workflow.
   - Example:
     ```python
     VISUALIZATION_SYSTEM_PROMPT = """You are an expert data visualization assistant specializing in Plotly..."""
     ```
   - Guides the agent on how to analyze data, choose chart types, and handle errors.

2. **Tools**: Functions that the agent uses to perform specific tasks.
   - `create_plotly_chart`: Generates Plotly charts.
   - `repair_plotly_code`: Fixes errors in Plotly code.
   - `get_dataframe_info`: Analyzes the structure of the input data.

3. **LangChain Integration**: Uses the `create_agent` API to initialize the agent.
   - Example:
     ```python
     agent = create_agent(llm, tools=tools, system_prompt=VISUALIZATION_SYSTEM_PROMPT)
     ```

---

## Code Walkthrough

### Agent Initialization
```python
def create_plotly_agent(model: str = "gpt-4o", temperature: float = 0.0, verbose: bool = False) -> Any:
    llm = init_chat_model(model, temperature=temperature)
    tools = [create_plotly_chart, repair_plotly_code, get_dataframe_info]
    agent = create_agent(llm, tools=tools, system_prompt=VISUALIZATION_SYSTEM_PROMPT)
    return agent
```
- **`init_chat_model`**: Initializes the language model.
- **`tools`**: Specifies the tools available to the agent.
- **`create_agent`**: Combines the model, tools, and system prompt to create the agent.

### Chart Creation Workflow
```python
def create_chart(self, data: Any, instruction: str, reset_history: bool = False) -> Dict[str, Any]:
    if reset_history:
        self.chat_history = []

    # Convert data to JSON
    data_json = json.dumps(data) if isinstance(data, (list, dict)) else data.to_json(orient='records')

    # Construct the message
    user_message = f"""Please create a visualization for the following data:\n\nDATA (JSON format):\n{data_json}\n\nINSTRUCTION:\n{instruction}"""

    # Invoke the agent
    response = self.agent.invoke({"messages": self.chat_history + [HumanMessage(content=user_message)]})
    return response
```
- Converts data to JSON format.
- Constructs a user message with the data and instruction.
- Invokes the agent to generate a response.

---

## Activity
1. Explore the `create_plotly_agent` function and identify the tools used.
2. Modify the `VISUALIZATION_SYSTEM_PROMPT` to add new capabilities.
3. Experiment with the `create_chart` method to understand its workflow.

---

## Summary
The `PlotlyVisualizationAgent` is built on a modular architecture that combines a system prompt, tools, and LangChain integration. Understanding its internal functionality helps in extending and customizing the agent.
