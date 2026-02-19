# Lesson 5: Implementing Security Guardrails for Agents

## Objective
In this lesson, students will learn how to implement security guardrails for AI agents. Using the `security.py` module, they will understand how to detect and prevent malicious code execution in the context of Plotly chart generation.

---

## Key Concepts

### Why Security Guardrails Are Important
- AI agents often execute user-provided code or instructions.
- Without proper safeguards, malicious code can compromise the system.
- Guardrails ensure that the agent operates safely and securely.

### Overview of `security.py`
- The `security.py` module uses Abstract Syntax Tree (AST) analysis to detect potentially dangerous code patterns.
- It identifies:
  - Dangerous functions (e.g., `exec`, `eval`)
  - Dangerous modules (e.g., `os`, `sys`)
  - Suspicious imports and attributes

---

## Code Walkthrough

### Malicious Code Detection
```python
class MaliciousCodeVisitor(ast.NodeVisitor):
    """AST visitor that detects potentially malicious code patterns."""

    DANGEROUS_FUNCTIONS = {"exec", "eval", "compile", "getattr", "setattr", "delattr", "globals", "locals", "__import__"}
    DANGEROUS_MODULES = {"os", "sys", "subprocess", "importlib", "shutil", "socket", "pickle", "shelve"}

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id in self.DANGEROUS_FUNCTIONS:
            self.warnings.append(f"Malicious code detected: {node.func.id}() on line {node.lineno}")
            self.malicious = True
```
- **`visit_Call`**: Detects calls to dangerous functions like `exec` and `eval`.
- **`DANGEROUS_FUNCTIONS`**: A set of functions that can execute arbitrary code.

### Checking for Dangerous Imports
```python
def visit_Import(self, node):
    for alias in node.names:
        if alias.name in self.DANGEROUS_MODULES:
            self.warnings.append(f"Dangerous import detected: {alias.name} on line {node.lineno}")
            self.malicious = True
```
- **`visit_Import`**: Detects imports of dangerous modules like `os` and `sys`.
- **`DANGEROUS_MODULES`**: A set of modules that can access the system.

### Main Function: `check_malicious_code`
```python
def check_malicious_code(code: str, verbose: bool = False) -> bool:
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
        return True
```
- **`ast.parse`**: Parses the code into an AST.
- **`MaliciousCodeVisitor`**: Visits each node in the AST to detect malicious patterns.
- **`verbose`**: Prints warnings if enabled.

---

## Activity
1. Write a Python script that uses the `check_malicious_code` function to analyze a code snippet.
2. Test the function with the following examples:
   - Safe code:
     ```python
     print("Hello, World!")
     ```
   - Malicious code:
     ```python
     exec("print('This is dangerous!')")
     ```
3. Modify the `DANGEROUS_FUNCTIONS` and `DANGEROUS_MODULES` sets to include additional patterns.

---

## Summary
The `security.py` module demonstrates how to implement security guardrails for AI agents. By analyzing code with AST, it ensures that potentially dangerous patterns are detected and mitigated before execution. This approach is essential for building secure and reliable AI systems.
