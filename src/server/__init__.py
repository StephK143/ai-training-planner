from flask import Flask
from flask_cors import CORS
from .routes import api_routes

def create_app():
    app = Flask(__name__)
    CORS(app)  # Enable CORS for all routes
    
    # Register blueprints
    app.register_blueprint(api_routes)
    
    return app

app = create_app()
