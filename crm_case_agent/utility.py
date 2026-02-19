def get_customer_cases(client, customer_name, top=10):
    """
    Retrieves customer cases from Dataverse based on customer name.
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
    if case.get('customerid_contact'):
        return case.get('customerid_contact', {}).get('fullname', 'N/A')
    elif case.get('customerid_account'):
        return case.get('customerid_account', {}).get('name', 'N/A')
    return 'N/A'

