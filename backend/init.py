from flask import Flask
from config import config
from models import db
from routes import users_bp

def create_app(config_name='development'):
    app = Flask(__name__)
    
    # Load the configuration based on the environment
    app.config.from_object(config[config_name])

    # Initialize the database with the app
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(users_bp)

    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()

    return app
