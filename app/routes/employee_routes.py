from flask import Blueprint, jsonify, request
from app.utils.logger import logger
from app.utils.validator import validate_employee
from app.services.employee_service import (
    create_employee,
    get_all_employees,
    get_employee_by_id,
    update_employee,
    delete_employee
)

employee_bp = Blueprint("employee", __name__)


@employee_bp.route("/")
def home():
    return jsonify({
        "message": "Welcome to Employee Management System API 🚀",
        "version": "1.0.0"
    })


@employee_bp.route("/health")
def health():
    return jsonify({
        "status": "UP",
        "message": "Employee Management API is running successfully"
    })


@employee_bp.route("/employees", methods=["POST"])
def add_employee():
    try:
        data = request.get_json()

        logger.info("Create employee request received")

        # Validate request
        is_valid, error = validate_employee(data)

        if not is_valid:
            logger.warning(error)
            return jsonify({
                "status": "error",
                "message": error
            }), 400

        # Save employee
        employee_id = create_employee(data)

        logger.info(f"Employee created successfully with ID {employee_id}")

        return jsonify({
            "status": "success",
            "message": "Employee created successfully",
            "employee_id": employee_id
        }), 201

    except ValueError as e:
        error_message = str(e)

        logger.warning(error_message)

        if "email" in error_message:
            return jsonify({
                "status": "error",
                "message": "Email already exists"
            }), 409

        if "employee_id" in error_message:
            return jsonify({
                "status": "error",
                "message": "Employee ID already exists"
            }), 409

        return jsonify({
            "status": "error",
            "message": error_message
        }), 400

    except Exception:
        logger.exception("Unexpected error while creating employee")
        return jsonify({
            "status": "error",
            "message": "Internal Server Error"
        }), 500


@employee_bp.route("/employees", methods=["GET"])
def get_employees():
    try:
        logger.info("Fetching all employees")

        employees = get_all_employees()

        return jsonify({
            "status": "success",
            "count": len(employees),
            "data": employees
        }), 200

    except Exception:
        logger.exception("Unexpected error while fetching employees")
        return jsonify({
            "status": "error",
            "message": "Internal Server Error"
        }), 500


@employee_bp.route("/employees/<int:employee_id>", methods=["GET"])
def get_employee(employee_id):
    try:
        logger.info(f"Fetching employee with ID {employee_id}")

        employee = get_employee_by_id(employee_id)

        if employee is None:
            logger.warning(f"Employee {employee_id} not found")
            return jsonify({
                "status": "error",
                "message": "Employee not found"
            }), 404

        return jsonify({
            "status": "success",
            "data": employee
        }), 200

    except Exception:
        logger.exception("Unexpected error while fetching employee")
        return jsonify({
            "status": "error",
            "message": "Internal Server Error"
        }), 500


@employee_bp.route("/employees/<int:employee_id>", methods=["PUT"])
def edit_employee(employee_id):
    try:
        logger.info(f"Update request received for employee {employee_id}")

        data = request.get_json()

        updated = update_employee(employee_id, data)

        if updated == 0:
            logger.warning(f"Employee {employee_id} not found for update")
            return jsonify({
                "status": "error",
                "message": "Employee not found"
            }), 404

        logger.info(f"Employee {employee_id} updated successfully")

        return jsonify({
            "status": "success",
            "message": "Employee updated successfully"
        }), 200

    except Exception:
        logger.exception("Unexpected error while updating employee")
        return jsonify({
            "status": "error",
            "message": "Internal Server Error"
        }), 500


@employee_bp.route("/employees/<int:employee_id>", methods=["DELETE"])
def remove_employee(employee_id):
    try:
        logger.info(f"Delete request received for employee {employee_id}")

        deleted = delete_employee(employee_id)

        if deleted == 0:
            logger.warning(f"Employee {employee_id} not found for deletion")
            return jsonify({
                "status": "error",
                "message": "Employee not found"
            }), 404

        logger.info(f"Employee {employee_id} deleted successfully")

        return jsonify({
            "status": "success",
            "message": "Employee deleted successfully"
        }), 200

    except Exception:
        logger.exception("Unexpected error while deleting employee")
        return jsonify({
            "status": "error",
            "message": "Internal Server Error"
        }), 500