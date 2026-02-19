# Lesson 7: Understanding Code Extraction Utilities

## Objective
In this lesson, students will learn how the `extract.py` module works to parse Python code from text responses. They will understand the utility functions provided and their use cases in extracting code blocks.

---

## Key Concepts

### Purpose of `extract.py`
- The `extract.py` module provides utilities to parse Python code from text, especially from markdown-style code blocks.
- It is useful for extracting code snippets from AI-generated responses or documentation.

### Core Functions
1. **`extract_python_code`**: Extracts a single Python code block from text.
2. **`extract_all_code_blocks`**: Extracts all code blocks (Python or generic) from text.

---

## Code Walkthrough

### Function: `extract_python_code`
```python
def extract_python_code(text: str) -> Optional[str]:
    """
    Extract Python code from a markdown code block.
    """
    # Try to match ```python ... ``` blocks first
    match = re.search(r'```python\s*(.*?)\s*```', text, re.DOTALL)
    if match:
        return match.group(1).strip()

    # Try to match generic ``` ... ``` blocks
    match = re.search(r'```\s*(.*?)\s*```', text, re.DOTALL)
    if match:
        return match.group(1).strip()

    return None
```
- **Purpose**: Extracts the first Python code block from the input text.
- **Regex Explanation**:
  - `r'```python\s*(.*?)\s*```'`: Matches code blocks starting with ` ```python `.
  - `re.DOTALL`: Allows the `.` to match newline characters.
- **Fallback**: If no ` ```python ` block is found, it tries to match generic ` ``` ` blocks.
- **Return Value**: The extracted code as a string, or `None` if no code block is found.

### Function: `extract_all_code_blocks`
```python
def extract_all_code_blocks(text: str) -> list:
    """
    Extract all code blocks from text.
    """
    pattern = r'```(?:python)?\s*(.*?)\s*```'
    matches = re.findall(pattern, text, re.DOTALL)
    return [m.strip() for m in matches if m.strip()]
```
- **Purpose**: Extracts all code blocks (Python or generic) from the input text.
- **Regex Explanation**:
  - `r'```(?:python)?\s*(.*?)\s*```'`: Matches both ` ```python ` and generic ` ``` ` blocks.
  - `(?:python)?`: Makes the `python` part optional.
- **Return Value**: A list of extracted code strings.

---

## Activity
1. Test the `extract_python_code` function with the following input:
   ```
   Here is some Python code:
   ```python
   print("Hello, World!")
   ```
   ```
   And here is some generic code:
   ```
   SELECT * FROM users;
   ```
   ```
2. Test the `extract_all_code_blocks` function with the same input.
3. Modify the regex patterns to extract code blocks with specific languages (e.g., `sql`, `javascript`).

---

## Summary
The `extract.py` module provides powerful utilities for parsing code blocks from text. By understanding the regex patterns and their use cases, students can adapt these functions for various text-processing tasks.
