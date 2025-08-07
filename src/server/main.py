# Main entry point for the Flask server

from . import app

if __name__ == '__main__':
    app.run(debug=True, port=5000)
