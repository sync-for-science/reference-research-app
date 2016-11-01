''' The application.
'''
import os

from flask import Flask


# Create and configured application
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SYNCHRONIZER_HOST'] = os.getenv('SYNCHRONIZER_HOST')
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
    extensions.db.init_app(app)
    extensions.sync.init_app(app)

    return app
