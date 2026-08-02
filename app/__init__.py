from flask import Flask
from app.routes.employee_routes import employee_bp

def create_app():
    app = Flask(__name__)

    # Register Blueprints
    app.register_blueprint(employee_bp)

    return app