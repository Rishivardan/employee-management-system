def validate_employee(data):
    required_fields = [
        "employee_id",
        "first_name",
        "last_name",
        "email",
        "phone",
        "department",
        "designation",
        "salary",
        "joining_date"
    ]

    for field in required_fields:
        if field not in data or data[field] in ("", None):
            return False, f"{field} is required"

    return True, None