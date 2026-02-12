def get_customer_cases(client, customer_name, top=10):
    """
    Retrieves customer cases from Dataverse based on customer name.

    Args:
        client: DataverseClient instance
        customer_name: Name of the customer to search for
        top: Maximum number of records to retrieve (default: 10)

    Returns:
        Generator yielding batches of cases
    """
    case_batches = client.get(
        "incident",
        select=[
            "incidentid",
            "title",
            "ticketnumber",
            "prioritycode",
            "statuscode",
            "createdon",
            "modifiedon",
            "description",
            "_customerid_value",
        ],
        expand=["customerid_contact($select=fullname)", "customerid_account($select=name)"],
        filter=f"customerid_contact/fullname eq '{customer_name}' or customerid_account/name eq '{customer_name}'",
        top=top,
    )

    return case_batches


def get_customer_name_from_case(case):
    """
    Extracts the customer name from a case record.

    Args:
        case: Case record dictionary

    Returns:
        Customer name string or 'N/A' if not found
    """
    if case.get('customerid_contact'):
        return case.get('customerid_contact', {}).get('fullname', 'N/A')
    elif case.get('customerid_account'):
        return case.get('customerid_account', {}).get('name', 'N/A')
    return 'N/A'


def print_case_details(case):
    """
    Prints formatted case details.

    Args:
        case: Case record dictionary
    """
    customer = get_customer_name_from_case(case)
    print(f"Customer: {customer}, Case: {case['title']}, Ticket Number: {case['ticketnumber']}, Priority: {case['prioritycode']}, Status: {case['statuscode']}, Created On: {case['createdon']}, Description: {case.get('description', 'N/A')}")

