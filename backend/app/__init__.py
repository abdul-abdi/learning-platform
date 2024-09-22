import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import config, generate_secret_key
from prometheus_flask_exporter import PrometheusMetrics
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
import logging

db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()
bcrypt = Bcrypt()
cache = Cache()
limiter = Limiter(key_func=get_remote_address)

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Ensure SECRET_KEY is set
    if not app.config['SECRET_KEY']:
        app.config['SECRET_KEY'] = generate_secret_key()
    
    # Log the secret key (be cautious with this in production)
    app.logger.info(f"Using SECRET_KEY: {app.config['SECRET_KEY']}")

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    cache.init_app(app)
    limiter.init_app(app)
    CORS(app)

    PrometheusMetrics(app)

    # Move Sentry initialization here
    sentry_sdk.init(
        dsn=app.config['SENTRY_DSN'],
        integrations=[FlaskIntegration()],
        traces_sample_rate=1.0
    )

    from .routes import auth_bp, learning_material_bp, user_progress_bp, dashboard_bp, protected_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(learning_material_bp)
    app.register_blueprint(user_progress_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(protected_bp)

    return app