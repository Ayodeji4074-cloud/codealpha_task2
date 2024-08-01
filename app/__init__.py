#importing all dependencies
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os
from datetime import timedelta

# Loading environment variables from .env file
load_dotenv()

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

    
#function that helps to access and use all config files    
def create_app(config_name=None):
    app = Flask(__name__)
    # for testing configurations
    if config_name == 'testing':
        app.config.from_object('app.config.TestingConfig')
    #for app configuration
    else:
        app.config.from_object('app.config.Config')

    
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    with app.app_context():
        from app.routes import bp as routes_bp
        app.register_blueprint(routes_bp)

    return app
