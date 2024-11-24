from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import config
from models import db
from routes.user_routes import users_bp
from routes.creator_routes import creator_bp  # Import new blueprint

migrate = Migrate()  # Initialize Flask-Migrate

def create_app(config_name='development'):
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])

    # Initialize database
    db.init_app(app)
    
    # Initialize migrations
    migrate.init_app(app, db)

    # Enable CORS for all routes
    CORS(app)

    # Register blueprints
    app.register_blueprint(users_bp)
    app.register_blueprint(creator_bp)  # Register creator routes

    return app
