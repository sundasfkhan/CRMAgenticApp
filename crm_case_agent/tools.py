from dataclasses import dataclass
from langchain.tools import tool, ToolRuntime
from crm_case_agent.utility import get_customer_cases, get_customer_name_from_case

# Maps for option set fields (fallback when Dataverse doesn't return formatted annotations)
PRIORITY_MAP = {
    1: "High",
    2: "Normal",
    3: "Low",
}

# Common status (state) mappings for the Case (incident) entity
# Renamed from STATE_MAP to STATUS_MAP to reflect 'status' (statecode) terminology
STATUS_MAP = {
    0: "Active",
    1: "Resolved",
    2: "Cancelled",
}

# Status reason (statuscode) mappings grouped under the above statuses
STATUS_REASON_MAP = {
     # Active reasons
     1: "In Progress",
     2: "On Hold",
     3: "Waiting for Details",
     4: "Researching",
     # Resolved reasons
     5: "Problem Solved",
     1000: "Information Provided",
     # Cancelled reasons
     6: "Cancelled",
     2000: "Merged",
 }

@dataclass
class CRMContext:
    dataverse_client: object

@tool
def retrieve_customer_cases(customer_name: str, runtime: ToolRuntime[CRMContext]) -> str:
    """
    Retrieves CRM cases for a specific customer by their name.
    This function will attempt to use formatted (display) values from Dataverse when available
    and fall back to mapping dictionaries when only numeric codes are returned.
    """
    dataverse_client = runtime.context.dataverse_client
    if dataverse_client is None:
        return "Error: Dataverse client not initialized."

    try:
        case_batches = get_customer_cases(dataverse_client, customer_name, top=50)
        cases_list = []
        for batch in case_batches:
            for case in batch:
                customer = get_customer_name_from_case(case)

                # Prefer formatted annotations if present for priority
                priority = case.get('prioritycode@OData.Community.Display.V1.FormattedValue')
                if not priority:
                    # Fall back to mapping by integer code
                    raw_priority = case.get('prioritycode')
                    try:
                        priority = PRIORITY_MAP.get(int(raw_priority)) if raw_priority is not None else 'N/A'
                    except Exception:
                        priority = raw_priority if raw_priority is not None else 'N/A'

                # Status (statecode) and Status Reason (statuscode) handling
                status = case.get('statecode@OData.Community.Display.V1.FormattedValue')
                raw_state = case.get('statecode')
                if not status:
                    try:
                        status = STATUS_MAP.get(int(raw_state)) if raw_state is not None else None
                    except Exception:
                        status = None

                status_reason = case.get('statuscode@OData.Community.Display.V1.FormattedValue')
                raw_status = case.get('statuscode')
                if not status_reason:
                    try:
                        status_reason = STATUS_REASON_MAP.get(int(raw_status)) if raw_status is not None else None
                    except Exception:
                        status_reason = None

                # If status missing, try to derive it from status_reason numeric code
                if not status:
                    derived = None
                    try:
                        code = int(raw_status) if raw_status is not None else None
                    except Exception:
                        code = None
                    if code is not None:
                        if code in (1, 2, 3, 4):
                            derived = "Active"
                        elif code in (5, 1000):
                            derived = "Resolved"
                        elif code in (6, 2000):
                            derived = "Cancelled"
                        else:
                            derived = STATUS_MAP.get(code)
                    status = status or derived or 'N/A'

                # Ensure non-empty values
                priority = priority or 'N/A'
                status = status or 'N/A'
                status_reason = status_reason or 'N/A'

                cases_list.append({
                    "customer": customer,
                    "title": case.get('title', 'N/A'),
                    "ticket_number": case.get('ticketnumber', 'N/A'),
                    "priority": priority,
                    "status": status,
                    "status_reason": status_reason,
                    "createdon": case.get('createdon'),
                    "description": case.get('description', 'N/A')
                })

        if not cases_list:
            return f"No cases found for customer: {customer_name}"

        result = f"Found {len(cases_list)} case(s) for '{customer_name}':\n\n"
        for i, case in enumerate(cases_list, 1):
            result += (
                f"{i}. **{case['title']}**\n"
                f"   - Ticket: {case['ticket_number']}\n"
                f"   - Priority: {case['priority']}\n"
                f"   - Status: {case['status']}\n"
                f"   - Status Reason: {case['status_reason']}\n\n"
            )
        return result

    except Exception as e:
        return f"Error retrieving cases: {str(e)}"
