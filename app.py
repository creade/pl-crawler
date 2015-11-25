from flask import Flask, request
from flask.ext.sqlalchemy import SQLAlchemy
from extensions import (
    db,
    migrate,
)
from views import blueprint
import os


def create_app(app_settings="config.ProductionConfig"):
    app = Flask(__name__)
    app.config.from_object(app_settings)
    register_extensions(app)
    register_blueprints(app)
    return app


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    return None

def register_blueprints(app):
    app.register_blueprint(blueprint)
    return None
