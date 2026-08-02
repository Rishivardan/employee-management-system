from app.database.db import get_connection
import pymysql


def create_employee(employee):
    """
    Insert a new employee into the database.
    """

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO employees (
            employee_id,
            first_name,
            last_name,
            email,
            phone,
            department,
            designation,
            salary,
            joining_date
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        employee["employee_id"],
        employee["first_name"],
        employee["last_name"],
        employee["email"],
        employee["phone"],
        employee["department"],
        employee["designation"],
        employee["salary"],
        employee["joining_date"]
    )

    try:
        cursor.execute(query, values)
        connection.commit()

        new_employee_id = cursor.lastrowid
        return new_employee_id

    except pymysql.err.IntegrityError as e:
        connection.rollback()
        raise ValueError(str(e)) from e

    finally:
        cursor.close()
        connection.close()

def get_all_employees():
    """
    Retrieve all employees from the database.
    """

    connection = get_connection()
    cursor = connection.cursor()

    query = "SELECT * FROM employees"

    cursor.execute(query)

    employees = cursor.fetchall()

    cursor.close()
    connection.close()

    return employees

def get_employee_by_id(employee_id):
    """
    Retrieve a single employee by ID.
    """

    connection = get_connection()
    cursor = connection.cursor()

    query = "SELECT * FROM employees WHERE id = %s"

    cursor.execute(query, (employee_id,))

    employee = cursor.fetchone()

    cursor.close()
    connection.close()

    return employee

def update_employee(employee_id, employee):
    """
    Update an existing employee.
    """

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        UPDATE employees
        SET
            first_name = %s,
            last_name = %s,
            email = %s,
            phone = %s,
            department = %s,
            designation = %s,
            salary = %s,
            joining_date = %s,
            status = %s
        WHERE id = %s
    """

    values = (
        employee["first_name"],
        employee["last_name"],
        employee["email"],
        employee["phone"],
        employee["department"],
        employee["designation"],
        employee["salary"],
        employee["joining_date"],
        employee["status"],
        employee_id
    )

    cursor.execute(query, values)
    connection.commit()

    updated_rows = cursor.rowcount

    cursor.close()
    connection.close()

    return updated_rows

def delete_employee(employee_id):
    """
    Delete an employee by ID.
    """

    connection = get_connection()
    cursor = connection.cursor()

    query = "DELETE FROM employees WHERE id = %s"

    cursor.execute(query, (employee_id,))
    connection.commit()

    deleted_rows = cursor.rowcount

    cursor.close()
    connection.close()

    return deleted_rows