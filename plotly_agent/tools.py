"""
Plotly chart tools for the visualization agent.

This module provides LangChain tools for creating and repairing Plotly charts
with built-in security checks.
"""

import json
import os
from datetime import datetime
import uuid
from typing import Any, Dict, Optional, Union
from langchain.tools import tool
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from .security import check_malicious_code


def _should_save_images() -> bool:
    """Check if SAVE_IMAGES environment variable is set to Yes."""
    save_images = os.environ.get("SAVE_IMAGES", "").strip().lower()
    return save_images in ("yes", "true", "1")


def _save_chart(fig, chart_type: str = "chart") -> Optional[str]:
    """
    Save a Plotly figure to the data folder if SAVE_IMAGES is enabled.

    Args:
        fig: Plotly figure object
        chart_type: Type of chart for filename prefix

    Returns:
        Path to saved file if saved, None otherwise
    """
    if not _should_save_images():
        return None

    try:
        # Get the project root directory (parent of plotly_agent)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        data_folder = os.path.join(project_root, "data")

        # Create data folder if it doesn't exist
        os.makedirs(data_folder, exist_ok=True)

        # Generate unique filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        filename = f"{chart_type}_{timestamp}_{unique_id}.html"
        filepath = os.path.join(data_folder, filename)

        # Save as HTML (interactive)
        fig.write_html(filepath)

        # Also save as PNG if kaleido is available
        try:
            png_filepath = filepath.replace(".html", ".png")
            fig.write_image(png_filepath)
            print(f"[INFO] Chart saved to: {filepath} and {png_filepath}")
            return filepath
        except Exception:
            # kaleido not installed, just save HTML
            print(f"[INFO] Chart saved to: {filepath}")
            return filepath

    except Exception as e:
        print(f"[WARNING] Failed to save chart: {e}")
        return None


@tool
def create_plotly_chart(data_json: str, plotly_code: str) -> str:
    """
    Create a Plotly chart from data and Python code.

    Use this tool to generate data visualizations. The code should create
    a figure object named 'fig' using plotly.express (px) or plotly.graph_objects (go).

    Args:
        data_json: JSON string representation of the DataFrame data.
                   Example: '[{"A": 1, "B": 2}, {"A": 3, "B": 4}]'
        plotly_code: Python code that creates a Plotly figure named 'fig'.
                     Example: 'fig = px.line(df, x="A", y="B", title="My Chart")'

    Returns:
        JSON string of the figure for rendering, or error message if failed.
    """
    try:
        # Parse the data
        if isinstance(data_json, str):
            data = json.loads(data_json)
        else:
            data = data_json
        df = pd.DataFrame(data)

        # Security check
        if check_malicious_code(plotly_code, verbose=True):
            return json.dumps({
                "error": "Security Error: Malicious code patterns detected. Please revise your code.",
                "success": False
            })

        # Create execution context
        exec_context = {
            "df": df,
            "px": px,
            "go": go,
            "pd": pd
        }

        # Execute the code
        exec(plotly_code, exec_context)
        fig = exec_context.get("fig")

        if fig is None:
            return json.dumps({
                "error": "The code did not create a 'fig' variable. Ensure your code assigns the figure to 'fig'.",
                "success": False
            })

        # Save chart if SAVE_IMAGES is enabled
        saved_path = _save_chart(fig, "chart")

        # Return figure as JSON for serialization
        result = {
            "figure_json": fig.to_json(),
            "success": True,
            "message": "Chart created successfully"
        }
        if saved_path:
            result["saved_path"] = saved_path

        return json.dumps(result)

    except Exception as e:
        return json.dumps({
            "error": f"Error creating chart: {str(e)}",
            "success": False,
            "original_code": plotly_code
        })


@tool
def repair_plotly_code(data_json: str, plotly_code: str, error_message: str) -> str:
    """
    Attempt to repair and execute Plotly code that previously failed.

    Use this tool when create_plotly_chart fails and you need to fix the code.

    Args:
        data_json: JSON string representation of the DataFrame data.
        plotly_code: The corrected Python code that creates a Plotly figure named 'fig'.
        error_message: The error message from the previous failed attempt.

    Returns:
        JSON string of the figure for rendering, or error message if repair failed.
    """
    try:
        # Parse the data
        if isinstance(data_json, str):
            data = json.loads(data_json)
        else:
            data = data_json
        df = pd.DataFrame(data)

        # Security check
        if check_malicious_code(plotly_code, verbose=True):
            return json.dumps({
                "error": "Security Error: Malicious code patterns detected in repair attempt.",
                "success": False
            })

        # Create execution context
        exec_context = {
            "df": df,
            "px": px,
            "go": go,
            "pd": pd,
            "previous_error": error_message
        }

        # Execute the repaired code
        exec(plotly_code, exec_context)
        fig = exec_context.get("fig")

        if fig is None:
            return json.dumps({
                "error": "Repair failed: The code still did not create a 'fig' variable.",
                "success": False,
                "previous_error": error_message
            })

        # Save chart if SAVE_IMAGES is enabled
        saved_path = _save_chart(fig, "repaired_chart")

        result = {
            "figure_json": fig.to_json(),
            "success": True,
            "message": "Chart repaired and created successfully"
        }
        if saved_path:
            result["saved_path"] = saved_path

        return json.dumps(result)

    except Exception as e:
        return json.dumps({
            "error": f"Repair failed: {str(e)}",
            "success": False,
            "previous_error": error_message,
            "attempted_code": plotly_code
        })


@tool
def get_dataframe_info(data_json: str) -> str:
    """
    Get information about a DataFrame to help with chart creation.

    Use this tool to understand the structure and content of the data
    before creating a chart.

    Args:
        data_json: JSON string representation of the DataFrame data.

    Returns:
        JSON string containing DataFrame information (columns, dtypes, sample data).
    """
    try:
        if isinstance(data_json, str):
            data = json.loads(data_json)
        else:
            data = data_json
        df = pd.DataFrame(data)

        info = {
            "columns": list(df.columns),
            "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
            "shape": {"rows": len(df), "columns": len(df.columns)},
            "sample_data": df.head(3).to_dict(orient="records"),
            "numeric_columns": list(df.select_dtypes(include=['number']).columns),
            "categorical_columns": list(df.select_dtypes(include=['object', 'category']).columns),
            "success": True
        }

        return json.dumps(info)

    except Exception as e:
        return json.dumps({
            "error": f"Error analyzing data: {str(e)}",
            "success": False
        })

