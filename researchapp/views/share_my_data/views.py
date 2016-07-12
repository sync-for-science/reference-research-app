""" Some views"""
from flask import (
    redirect,
    render_template,
    request,
    url_for,
)
from injector import inject
from werkzeug.exceptions import Forbidden

from researchapp.blueprints import share_my_data
from researchapp.services import authorize, resources
from researchapp.models.participants import THE_ONLY_PARTICIPANT_ID


@share_my_data.route('/')
def view_index():
    """ Homepage.
    """
    return render_template('home.jinja2', project='ResearchApp')


@share_my_data.route('/share-my-data')
def view_share_my_data():
    """ Share my data.
    """
    return render_template('share_my_data.jinja2')


@share_my_data.route('/consent')
@inject(service=authorize.AuthorizeService)
def view_consent(service):
    """ Consent page.
    """
    view_data = service.display_consent(request.args['doctor'])

    return render_template('consent.jinja2', **view_data)


@share_my_data.route('/connected')
@inject(service=resources.ResourceService)
def view_connected(service):
    """ Show all connected providers.
    """
    connections = service.display_connections(THE_ONLY_PARTICIPANT_ID)

    return render_template('connected.jinja2', connections=connections)


@share_my_data.route('/authorized')
@inject(service=authorize.AuthorizeService)
def authorized(service):
    """ Handle authorized callback.
    """
    try:
        service.register_authorization(request.url)
    except authorize.FHIRUnauthorizedException:
        raise Forbidden()

    return redirect(url_for('.view_connected'))
