from flask import Flask
from flask_cors import CORS
from config import config
from models import db
from routes import users_bp

def create_app(config_name='development'):
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])

    # Initialize database
    db.init_app(app)
    
    # Enable CORS for all routes
    CORS(app)

    # Register blueprints
    app.register_blueprint(users_bp)

    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()

    return app
