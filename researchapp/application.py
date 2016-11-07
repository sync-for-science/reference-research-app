''' The application.
'''
import os

from flask import Flask


# Create and configured application
app = Flask(__name__)
app.config['SYNCHRONIZER_HOST'] = os.getenv('SYNCHRONIZER_HOST')
app.config['SYNCHRONIZER_USER'] = os.getenv('SYNCHRONIZER_USER')
app.config['SYNCHRONIZER_PASS'] = os.getenv('SYNCHRONIZER_PASS')
app.secret_key = os.getenv('FLASK_SECRET_KEY')


def create_app():
    ''' The application factory.
    '''
    from researchapp import (
        extensions,
    )
    from researchapp.views.consent.views import BP as consent_blueprint

    # Register blueprints
    app.register_blueprint(consent_blueprint)

    # Init extensions
    extensions.sync.init_app(app)

    return app
