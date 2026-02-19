# CRM Case Agent - Capabilities Guide

A comprehensive guide to the CRM Case Agent built with LangChain and Microsoft Dynamics 365 Dataverse.

## Overview

The CRM Case Agent is an AI-powered assistant that interacts with Microsoft Dynamics 365 CRM data using natural language. It leverages OpenAI's language models and LangChain's agent framework to provide intelligent case management capabilities.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      CRM Case Agent                         │
├─────────────────────────────────────────────────────────────┤
│  LangChain Agent (GPT-4o)                                   │
│       ↓                                                     │
│  Tools (retrieve_customer_cases, etc.)                      │
│       ↓                                                     │
│  Dataverse Client                                           │
│       ↓                                                     │
│  Microsoft Dynamics 365 CRM (Web API)                       │
└─────────────────────────────────────────────────────────────┘
```

## Current Capabilities

### 1. Retrieve Customer Cases

Retrieves CRM cases/incidents for a specific customer by name.

**Tool:** `retrieve_customer_cases`

**Usage Examples:**
- "Show me all cases for Contoso Ltd"
- "What support tickets does John Smith have?"
- "Find incidents for Trey Research"

**Returns:**
- Case title
- Ticket number
- Status
- Customer name

---

## Additional Capabilities (Can Be Added)

### 2. Create New Cases

Creates a new support case for a customer.

```python
@tool
def create_case(customer_name: str, title: str, description: str, priority: int, runtime: ToolRuntime[CRMContext]) -> str:
    """
    Creates a new support case for a customer.
    
    Args:
        customer_name: Customer name to associate the case with
        title: Case title/subject
        description: Detailed description of the issue
        priority: Priority level (1=High, 2=Normal, 3=Low)
    """
    # Implementation here
    pass
```

**Usage Examples:**
- "Create a new high priority case for Contoso about billing issue"
- "Open a support ticket for John Smith regarding login problems"

---

### 3. Update Case Status

Updates the status of an existing case.

```python
@tool
def update_case_status(ticket_number: str, new_status: str, runtime: ToolRuntime[CRMContext]) -> str:
    """
    Updates the status of an existing case.
    
    Args:
        ticket_number: The case ticket number
        new_status: New status (Active, Resolved, Cancelled)
    """
    # Implementation here
    pass
```

**Usage Examples:**
- "Mark case CAS-001234 as resolved"
- "Change status of ticket CAS-005678 to active"

---

### 4. Search Customers

Searches for customers (accounts or contacts) by name or email.

```python
@tool
def search_customers(search_term: str, runtime: ToolRuntime[CRMContext]) -> str:
    """
    Searches for customers (accounts or contacts) by name or email.
    
    Args:
        search_term: Name or email to search for
    """
    # Implementation here
    pass
```

**Usage Examples:**
- "Find customer with email john@contoso.com"
- "Search for accounts containing 'Microsoft'"

---

### 5. Get Case Notes/Activities

Retrieves notes and activities for a specific case.

```python
@tool
def get_case_notes(ticket_number: str, runtime: ToolRuntime[CRMContext]) -> str:
    """
    Retrieves notes and activities for a specific case.
    
    Args:
        ticket_number: The case ticket number
    """
    # Implementation here
    pass
```

**Usage Examples:**
- "Show me notes for case CAS-001234"
- "What activities are logged on ticket CAS-005678?"

---

### 6. Add Note to Case

Adds a note to an existing case.

```python
@tool
def add_case_note(ticket_number: str, note_text: str, runtime: ToolRuntime[CRMContext]) -> str:
    """
    Adds a note to an existing case.
    
    Args:
        ticket_number: The case ticket number
        note_text: The note content to add
    """
    # Implementation here
    pass
```

**Usage Examples:**
- "Add a note to case CAS-001234 saying 'Customer called for follow-up'"
- "Log an update on ticket CAS-005678"

---

### 7. Get Case Statistics

Retrieves case statistics like open cases, resolved cases, average resolution time.

```python
@tool
def get_case_statistics(runtime: ToolRuntime[CRMContext]) -> str:
    """
    Retrieves case statistics like open cases, resolved cases, average resolution time.
    """
    # Implementation here
    pass
```

**Usage Examples:**
- "How many open cases do we have?"
- "Show me case statistics for this month"

---

### 8. Assign Case

Assigns a case to a specific user or team.

```python
@tool
def assign_case(ticket_number: str, assignee: str, runtime: ToolRuntime[CRMContext]) -> str:
    """
    Assigns a case to a specific user or team.
    
    Args:
        ticket_number: The case ticket number
        assignee: User or team name to assign the case to
    """
    # Implementation here
    pass
```

**Usage Examples:**
- "Assign case CAS-001234 to Support Team A"
- "Transfer ticket CAS-005678 to John Doe"

---

### 9. Escalate Case

Escalates a case to higher priority or management.

```python
@tool
def escalate_case(ticket_number: str, reason: str, runtime: ToolRuntime[CRMContext]) -> str:
    """
    Escalates a case to higher priority.
    
    Args:
        ticket_number: The case ticket number
        reason: Reason for escalation
    """
    # Implementation here
    pass
```

**Usage Examples:**
- "Escalate case CAS-001234 due to SLA breach"
- "Mark ticket CAS-005678 as urgent"

---

## Capabilities Summary Table

| Tool | Description | Status |
|------|-------------|--------|
| `retrieve_customer_cases` | Get cases for a customer | ✅ Implemented |
| `create_case` | Create new support case | 🔲 To Add |
| `update_case_status` | Update case status | 🔲 To Add |
| `search_customers` | Search accounts/contacts | 🔲 To Add |
| `get_case_notes` | View case history | 🔲 To Add |
| `add_case_note` | Add comments to cases | 🔲 To Add |
| `get_case_statistics` | Dashboard/reporting | 🔲 To Add |
| `assign_case` | Route cases to agents | 🔲 To Add |
| `escalate_case` | Increase priority | 🔲 To Add |

---

## Dynamics 365 Dataverse Entities Reference

| Entity | API Name | Description |
|--------|----------|-------------|
| Cases | `incidents` | Customer service cases |
| Accounts | `accounts` | Business customers |
| Contacts | `contacts` | Individual customers |
| Opportunities | `opportunities` | Sales opportunities |
| Leads | `leads` | Potential customers |
| Notes | `annotations` | Notes/attachments |
| Activities | `activitypointers` | All activity types |

---

## Environment Setup

### Required Environment Variables

Create a `.env` file with the following:

```dotenv
# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key-here

# Dataverse/Dynamics 365 Configuration
DATAVERSE_RESOURCE_URL=https://your-org.crm.dynamics.com
AZURE_TENANT_ID=your-tenant-id
AZURE_CLIENT_ID=your-client-id
AZURE_CLIENT_SECRET=your-client-secret
```

### Dependencies

```bash
pip install -r requirements.txt
```

---

## Usage

### Interactive Chat Mode

```python
from crm_case_agent import CRMCaseAgent

# Initialize with your Dataverse client
agent = CRMCaseAgent(dataverse_client)

# Start interactive chat
agent.chat()
```

### Programmatic Usage

```python
from crm_case_agent import CRMCaseAgent

agent = CRMCaseAgent(dataverse_client)

# Single query
response = agent.run("Show me all cases for Contoso Ltd")
print(response)
```

---

## Sample Conversations

**User:** "Show me all open cases for Trey Research"
**Agent:** "Found 3 case(s) for 'Trey Research':
1. Network connectivity issue (Ticket: CAS-001234) - Status: Active
2. Software installation request (Ticket: CAS-001235) - Status: In Progress
3. Password reset needed (Ticket: CAS-001236) - Status: Waiting"

**User:** "What's the status of ticket CAS-001234?"
**Agent:** "Case CAS-001234 is currently Active with high priority. It was created on 2024-01-15 and is assigned to Support Team A."

---

## Best Practices

1. **Always verify customer names** before creating or updating cases
2. **Use ticket numbers** for specific case operations
3. **Include context** when adding notes to cases
4. **Check case status** before making updates

---

## Contributing

To add new capabilities:

1. Create a new `@tool` decorated function in `crm_case_agent.py`
2. Add the tool to the `tools` list in `create_agent()`
3. Update this documentation

---

## License

[Your License Here]

