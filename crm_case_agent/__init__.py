"""CRM Case Agent package

This package contains the refactored CRM case agent implementation.
Exports:
- CRMCaseAgent
- retrieve_customer_cases
"""
from .agent import CRMCaseAgent
from .tools import retrieve_customer_cases

__all__ = ["CRMCaseAgent", "retrieve_customer_cases"]

