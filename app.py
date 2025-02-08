# app.py

from routes import app  # Import the Flask app instance defined in routes.py

if __name__ == '__main__':
    # Run the Flask development server.
    # Set debug=True if you want automatic reloads during development.
    app.run(host='0.0.0.0', port=5000, debug=True)
