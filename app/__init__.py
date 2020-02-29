import os
from flask import Flask, jsonify, g
from flask_sqlalchemy import SQLAlchemy
from .decorators import json, no_cache
from flask_cors import CORS, cross_origin
from flask_limit import RateLimiter
from flask_redis import FlaskRedis


db = SQLAlchemy()
limiter = RateLimiter()
redis_client = FlaskRedis()


def create_app(config_name):
    """Create an application instance."""
    app = Flask(__name__)

    # apply configuration
    cfg = os.path.join(os.getcwd(), 'config', config_name + '.py')
    app.config.from_pyfile(cfg)

    # initialize extensions
    db.init_app(app)
    limiter.init_app(app)
    redis_client.init_app(app)
    CORS(app)

    # register blueprints
    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    # register an after request handler
    @app.after_request
    def after_request(rv):
        headers = getattr(g, 'headers', {})
        rv.headers.extend(headers)
        return rv

    return app
