"""
Security module for detecting malicious code in Plotly chart generation.

This module provides AST-based analysis to detect potentially dangerous
code patterns before execution.
"""

import ast
from typing import Set


class MaliciousCodeVisitor(ast.NodeVisitor):
    """AST visitor that detects potentially malicious code patterns."""

    # Dangerous functions that could be used for code injection
    DANGEROUS_FUNCTIONS: Set[str] = {
        "exec", "eval", "compile", "getattr", "setattr",
        "delattr", "globals", "locals", "__import__"
    }

    # Dangerous modules that could be used for system access
    DANGEROUS_MODULES: Set[str] = {
        "os", "sys", "subprocess", "importlib", "shutil",
        "socket", "pickle", "shelve"
    }

    def __init__(self):
        self.malicious = False
        self.warnings: list = []

    def visit_Call(self, node):
        """Check for calls to dangerous functions."""
        if isinstance(node.func, ast.Name) and node.func.id in self.DANGEROUS_FUNCTIONS:
            self.warnings.append(
                f"Malicious code detected: {node.func.id}() on line {node.lineno}"
            )
            self.malicious = True
        self.generic_visit(node)

    def visit_Import(self, node):
        """Warn about potentially dangerous imports."""
        for alias in node.names:
            if alias.name in self.DANGEROUS_MODULES:
                self.warnings.append(
                    f"Dangerous import detected: {alias.name} on line {node.lineno}"
                )
                self.malicious = True
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        """Warn about imports from dangerous modules."""
        if node.module and node.module in self.DANGEROUS_MODULES:
            self.warnings.append(
                f"Dangerous import detected: {node.module} on line {node.lineno}"
            )
            self.malicious = True
        self.generic_visit(node)

    def visit_Attribute(self, node):
        """Detect use of dangerous attributes like exec or eval."""
        if isinstance(node.value, ast.Name) and node.attr in {"exec", "eval", "compile"}:
            self.warnings.append(
                f"Dynamic execution via {node.attr} detected on line {node.lineno}"
            )
            self.malicious = True
        self.generic_visit(node)


def check_malicious_code(code: str, verbose: bool = False) -> bool:
    """
    Check if the provided code contains malicious patterns.

    Args:
        code: The Python code string to analyze
        verbose: If True, print warnings for detected issues

    Returns:
        True if malicious patterns are detected, False otherwise
    """
    try:
        tree = ast.parse(code)
        visitor = MaliciousCodeVisitor()
        visitor.visit(tree)

        if verbose and visitor.warnings:
            for warning in visitor.warnings:
                print(f"[Security Warning] {warning}")

        return visitor.malicious
    except SyntaxError as e:
        if verbose:
            print(f"[Security Warning] Syntax error in code: {e}")
        return True  # Treat syntax errors as potentially malicious

