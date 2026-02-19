# Lesson 8: Understanding the Agent Code

## Objective
In this lesson, students will learn how the `agent.py` file implements the `PlotlyVisualizationAgent`. They will explore the structure, key components, and workflow of the agent, including its integration with LangChain and tools.

---

## Key Concepts

### Purpose of `agent.py`
- Implements the `PlotlyVisualizationAgent` class for creating data visualizations.
- Uses the LangChain framework to integrate tools and manage interactions.
- Provides a high-level interface for generating charts and interacting with users.

### Core Components
1. **System Prompt**: Defines the agent's capabilities and workflow.
2. **Agent Initialization**: Sets up the LangChain agent with tools and a system prompt.
3. **Chart Creation**: Handles data and instructions to generate visualizations.
4. **Interactive Session**: Allows users to interact with the agent in a conversational manner.
5. **Error Handling**: Manages errors during chart creation and provides meaningful feedback.

---

## Code Walkthrough

### System Prompt
```python
VISUALIZATION_SYSTEM_PROMPT = """You are an expert data visualization assistant specializing in Plotly...
"""
```
- **Purpose**: Guides the agent on how to analyze data, choose chart types, and handle errors.
- **Capabilities**:
  - Analyze data structure.
  - Choose appropriate chart types.
  - Generate Plotly visualizations.
  - Repair code when errors occur.

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

### `PlotlyVisualizationAgent` Class
```python
class PlotlyVisualizationAgent:
    def __init__(self, model: str = "gpt-4o", temperature: float = 0.0, api_key: Optional[str] = None):
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key

        self.model = model
        self.temperature = temperature
        self.agent = create_plotly_agent(model=model, temperature=temperature)
        self.chat_history: List = []
```
- **Initialization**:
  - Sets up the agent with the specified model and temperature.
  - Stores the chat history for interactive sessions.

### Chart Creation
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
- **Data Conversion**: Converts input data to JSON format.
- **Message Construction**: Creates a user message with the data and instruction.
- **Agent Invocation**: Sends the message to the agent and receives a response.

### Interactive Session
```python
def interactive_session(self):
    print("Plotly Visualization Agent Ready (LangChain v1)")
    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in ['quit', 'exit']:
            print("Goodbye!")
            break
        response = self.chat(user_input)
        print(f"\nAgent: {response}")
```
- **Purpose**: Allows users to interact with the agent in real-time.
- **Features**:
  - Accepts user input.
  - Processes the input and generates a response.
  - Ends the session when the user types `quit` or `exit`.

### Error Handling
```python
def chat(self, message: str) -> str:
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
```
- **Purpose**: Handles errors during agent interaction.
- **Features**:
  - Updates chat history.
  - Returns error messages if an exception occurs.

---

## Activity
1. Modify the `VISUALIZATION_SYSTEM_PROMPT` to add new capabilities (e.g., support for additional chart types).
2. Test the `create_chart` method with different datasets and instructions.
3. Start an interactive session and explore the agent's responses to various queries.
4. Introduce an error in the input data and observe how the agent handles it.

---

## Summary
The `agent.py` file implements the `PlotlyVisualizationAgent` class, which combines the LangChain framework, tools, and a system prompt to create a powerful data visualization assistant. By understanding its structure and workflow, students can extend and customize the agent for their own use cases.
