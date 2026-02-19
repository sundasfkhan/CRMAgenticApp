# Lesson 3: Error Handling and Debugging

## Objective
In this lesson, students will learn how the `PlotlyVisualizationAgent` handles errors during chart creation and how to debug issues effectively.

---

## Key Concepts

### Error Handling
- The agent uses the `repair_plotly_code` tool to fix errors in Plotly code.
- Errors are captured and returned in the response dictionary.

### Debugging Steps
1. Check the `error` field in the response.
2. Analyze the error message.
3. Modify the input data or instruction if necessary.

---

## Code Walkthrough

### Example: Handling Errors
```python
# Intentionally provide incorrect data
invalid_data = {"InvalidKey": [1, 2, 3]}

result = agent.create_chart(
    data=invalid_data,
    instruction="Create a pie chart"
)

if not result["success"]:
    print(f"Error: {result['error']}")
```

### Example: Debugging
```python
# Print the raw response for debugging
print("Raw Response:", result)

# Check the error field
if not result["success"]:
    print("Error Message:", result.get("error", "Unknown error"))
```

---

## Activity
1. Provide invalid data to the `create_chart` method and observe the error message.
2. Modify the data or instruction to resolve the error.
3. Experiment with different types of errors (e.g., missing columns, invalid chart types).

---

## Summary
Error handling is an essential part of working with the `PlotlyVisualizationAgent`. By understanding how to debug issues, students can create robust and error-free visualizations.
