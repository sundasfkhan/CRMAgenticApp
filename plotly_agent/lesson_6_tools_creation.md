# Lesson 6: Creating Tools for Plotly Agents

## Objective
In this lesson, students will learn how to create tools for the Plotly agent. They will explore the `tools.py` module and understand how tools like `create_plotly_chart`, `repair_plotly_code`, and `get_dataframe_info` are implemented.

---

## Key Concepts

### What Are Tools?
- Tools are functions that the agent can use to perform specific tasks.
- In the context of LangChain, tools are decorated with the `@tool` decorator.
- Examples of tools in `tools.py`:
  - `create_plotly_chart`: Generates charts from data and code.
  - `repair_plotly_code`: Repairs Plotly code that failed to execute.
  - `get_dataframe_info`: Analyzes the structure of a DataFrame.

### Why Are Tools Important?
- Tools extend the functionality of the agent.
- They allow the agent to interact with data and perform complex operations.
- Tools ensure modularity and reusability.

---

## Code Walkthrough

### Tool: `create_plotly_chart`
```python
@tool
def create_plotly_chart(data_json: str, plotly_code: str) -> str:
    """
    Create a Plotly chart from data and Python code.
    """
    # Parse the data
    df = pd.DataFrame(json.loads(data_json))

    # Security check
    if check_malicious_code(plotly_code, verbose=True):
        return json.dumps({"error": "Malicious code detected.", "success": False})

    # Execute the code
    exec_context = {"df": df, "px": px, "go": go}
    exec(plotly_code, exec_context)
    fig = exec_context.get("fig")

    # Save and return the chart
    saved_path = _save_chart(fig, "chart")
    return json.dumps({"figure_json": fig.to_json(), "success": True, "saved_path": saved_path})
```
- **Purpose**: Generates a Plotly chart based on user-provided data and code.
- **Security**: Uses `check_malicious_code` to prevent unsafe code execution.
- **Output**: Returns the chart as JSON and saves it if enabled.

### Tool: `repair_plotly_code`
```python
@tool
def repair_plotly_code(data_json: str, plotly_code: str, error_message: str) -> str:
    """
    Attempt to repair and execute Plotly code that previously failed.
    """
    # Parse the data
    df = pd.DataFrame(json.loads(data_json))

    # Security check
    if check_malicious_code(plotly_code, verbose=True):
        return json.dumps({"error": "Malicious code detected in repair attempt.", "success": False})

    # Execute the repaired code
    exec_context = {"df": df, "px": px, "go": go}
    exec(plotly_code, exec_context)
    fig = exec_context.get("fig")

    # Save and return the repaired chart
    saved_path = _save_chart(fig, "repaired_chart")
    return json.dumps({"figure_json": fig.to_json(), "success": True, "saved_path": saved_path})
```
- **Purpose**: Repairs Plotly code that failed to execute.
- **Error Handling**: Uses the `error_message` to guide the repair process.
- **Output**: Returns the repaired chart as JSON.

### Tool: `get_dataframe_info`
```python
@tool
def get_dataframe_info(data_json: str) -> str:
    """
    Get information about a DataFrame to help with chart creation.
    """
    df = pd.DataFrame(json.loads(data_json))
    info = {
        "columns": list(df.columns),
        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
        "shape": {"rows": len(df), "columns": len(df.columns)},
        "sample_data": df.head(3).to_dict(orient="records")
    }
    return json.dumps(info)
```
- **Purpose**: Provides insights into the structure and content of the data.
- **Output**: Returns column names, data types, shape, and sample data.

---

## Activity
1. Create a new tool that generates a histogram from a DataFrame.
2. Modify the `create_plotly_chart` tool to include additional security checks.
3. Test the `get_dataframe_info` tool with different datasets.

---

## Summary
Tools are the building blocks of the Plotly agent's functionality. By understanding how tools are implemented, students can extend the agent's capabilities and create new tools for specific tasks.
