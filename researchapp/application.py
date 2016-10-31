''' The application.
'''
from flask import Flask


# Create and configured application
app = Flask(__name__)


def create_app():
    ''' The application factory.
    '''
    from researchapp.views.consent.views import BP as consent_blueprint

    # Register blueprints
    app.register_blueprint(consent_blueprint)

    return app
