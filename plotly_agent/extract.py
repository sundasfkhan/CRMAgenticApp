"""
Code extraction utilities for parsing Python code from LLM responses.
"""

import re
from typing import Optional


def extract_python_code(text: str) -> Optional[str]:
    """
    Extract Python code from a markdown code block.

    Args:
        text: The text containing potential Python code blocks

    Returns:
        The extracted Python code, or None if no code block is found
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


def extract_all_code_blocks(text: str) -> list:
    """
    Extract all code blocks from text.

    Args:
        text: The text containing potential code blocks

    Returns:
        List of extracted code strings
    """
    pattern = r'```(?:python)?\s*(.*?)\s*```'
    matches = re.findall(pattern, text, re.DOTALL)
    return [m.strip() for m in matches if m.strip()]
