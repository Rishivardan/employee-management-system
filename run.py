from app import create_app
from app.database.db import get_connection

app = create_app()

try:
    connection = get_connection()
    print("✅ Database connected successfully!")
    connection.close()
except Exception as e:
    print("❌ Database connection failed!")
    print(e)

if __name__ == "__main__":
    app.run(debug=True)