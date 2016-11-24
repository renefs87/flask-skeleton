from flask import Flask

from app.api.v1 import example_api_v1_bp, API_VERSION_V1
from app.common.google_auth import load_flask_dance_authorization
from app.extensions import db, security, api
from app.models import user_datastore
from app.static_assets import register_assets


def create_app(config):
    application = Flask(__name__)
    application.config.from_object(config)

    application.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app=application)
    security.init_app(app=application, datastore=user_datastore)
    api.init_app(app=application)

    if application.config.get('DEBUG', False):
        _load_sample_data(application)

    _load_application_blueprints(application)

    _load_api_module(application)

    load_flask_dance_authorization(application)

    register_assets(application)

    return application


def _load_application_blueprints(application):
    from app.views.common import common_bp
    application.register_blueprint(common_bp)

    from app.views.users import module as module_users
    application.register_blueprint(module_users)


def _load_api_module(application):
    application.register_blueprint(
        example_api_v1_bp, url_prefix='{prefix}/v{version}'.format(
            prefix=application.config['API_URL_PREFIX'],
            version=API_VERSION_V1))


def _load_sample_data(application):
    from app.models.initializers import users
    with application.app_context():
        users.add_initial_roles_to_database()

