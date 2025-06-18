from flask import Flask
from .db import db, migrate
from .models import task, goal
from .routes.task_routes import bp as tasks_bp
from .routes.goal_routes import bp as goals_bp
import os
from dotenv import load_dotenv
import logging
from logging.config import dictConfig
from flask_cors import CORS


load_dotenv()


def create_app(config=None):
    app = Flask(__name__)
    # CORS(app) # Enable CORS for all routes

    # configure_logging(app)
    configure_logging(app)
    logger = logging.getLogger(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')

    if config:
        # Merge `config` into the app's configuration
        # to override the app's default settings for testing
        app.config.update(config)

    try:
        db.init_app(app)
        migrate.init_app(app, db)
        logger.info("Database initialized successfully.")

        with app.app_context():
            # db.session.execute("SELECT 1")
            logger.info("DB connection test passed")
    except Exception as e:
        logger.exception("Error during DB initialization or connection")

    # Register Blueprints 
    app.register_blueprint(tasks_bp)
    app.register_blueprint(goals_bp)
    
    # configure_logging(app)

    configure_logging(app)
    logger = logging.getLogger(__name__)

    return app


def configure_logging(app):
    # Clear any default Flask handlers (useful for avoiding duplicate logs)
    for handler in app.logger.handlers:
        app.logger.removeHandler(handler)

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]',
        handlers=[
            logging.StreamHandler(),  # logs to console
            logging.FileHandler("app.log")  # log to file
        ]
    )

    # log Flask startup
    logging.getLogger().info("Logging is set up.")
