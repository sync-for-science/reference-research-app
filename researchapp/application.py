""" Holds the create_app() Flask application factory.
More information in create_app() docstirng.
"""
from importlib import import_module
import json
import os

from flask import Flask
import yaml

import researchapp as app_root
from researchapp.blueprints import all_blueprints
from researchapp.extensions import db

APP_ROOT_FOLDER = os.path.abspath(os.path.dirname(app_root.__file__))
TEMPLATE_FOLDER = os.path.join(APP_ROOT_FOLDER, 'templates')
STATIC_FOLDER = os.path.join(APP_ROOT_FOLDER, 'static')


def get_config(config_class_string, yaml_files=None):
    """ Load the Flask config from a class.

    Args:
        config_class_string (string): a configuration class that will be
            loaded (e.g. 'pypi_portal.config.Production')
        yaml_files (list): YAML files to load. This is for testing, leave
            None in dev/production.

    Returns:
        A class object ot be fed into app.config.from_object().
    """
    config_module, config_class = config_class_string.rsplit('.', 1)
    config_class_object = getattr(import_module(config_module), config_class)
    config_obj = config_class_object()

    # Expand some options
    db_fmt = 'researchapp.models.{0}'
    if getattr(config_obj, 'DB_MODELS_IMPORTS', False):
        config_obj.DB_MODELS_IMPORTS = [db_fmt.format(m) for m in config_obj.DB_MODELS_IMPORTS]

    # Load additional configuration settings.
    yaml_files = yaml_files or [f for f in [
        os.path.join('/', 'etc', 'pypi_portal', 'config.yml'),
        os.path.abspath(os.path.join(APP_ROOT_FOLDER, '..', 'config.yml')),
        os.path.join(APP_ROOT_FOLDER, 'config.yml'),
    ] if os.path.exists(f)]
    additional_dict = dict()
    for path in yaml_files:
        with open(path) as handle:
            additional_dict.update(yaml.load(handle.read()))

    return config_obj


def create_app(config_obj, no_sql=False):
    """ Flask application factory. Initializes and returns the Flask
    application.

    Modeled after: http://flask.pocoo.org/docs/patterns/appfactories/

    Args:
        config_obj: configuration object to load into app.config.
        no_sql: does not run init_app() for the SQLAlchemy instance. For Celery compatibility.

    Returns:
        The initialized Flask application.
    """
    # Initialize app. Flatten config_obj to dictionary (resolve properties).
    app = Flask(__name__, template_folder=TEMPLATE_FOLDER, static_folder=STATIC_FOLDER)
    config_dict = dict([(k, getattr(config_obj, k)) for k in dir(config_obj)
                        if not k.startswith('_')])
    app.config.update(config_dict)

    # Import DB models. Flask-SQLAlchemy doesn't do this automatically.
    with app.app_context():
        for module in app.config.get('DB_MODELS_IMPORTS', list()):
            import_module(module)

    # Setup and register views.
    for bpt in all_blueprints:
        import_module(bpt.import_name)
        app.register_blueprint(bpt)

    # Initialize extensions/add-ons/plugins.
    if not no_sql:
        db.init_app(app)

    # Define extra jinja2 filters
    @app.template_filter('prettify_json')
    def prettify_json(json_str):  # pylint: disable=unused-variable
        """ Reads a JSON string and returns it in a human-readable format.
        """
        data = json.loads(json_str)
        return json.dumps(data, indent=4)

    # Return the application instance.
    return app
