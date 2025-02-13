# app.py

from routes import app  # Import the Flask app instance defined in routes.py
import os
from dotenv import load_dotenv

if __name__ == '__main__':
    # Load environment variables from .env file
    load_dotenv()
    # Run the Flask development server.
    # Set debug=True if you want automatic reloads during development.
    port = int(os.getenv("PORT", 5000))
    print(f"Running on port {port}")
    debug = os.getenv("DEBUG", False)
    app.run(host='0.0.0.0', port=port, debug=debug)
