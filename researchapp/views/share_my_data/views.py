""" Some views"""
from flask import (
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)
from injector import inject
from werkzeug.exceptions import Forbidden

from researchapp.blueprints import share_my_data
from researchapp.services import authorize


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
    data = service.display_consent(request.args['doctor'])

    return render_template('consent.jinja2', **data)


@share_my_data.route('/connected')
def view_connected():
    """ Show all connected providers.
    """
    from researchapp.services.participants import participant_service
    from researchapp.services.resources import resource_service

    participant = participant_service().get_participant(1)
    connections = resource_service().find_all_for_participant(participant)

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

    return redirect(url_for('share_my_data.views.view_connected'))


@share_my_data.route('/fhir/<resource_type>')
def fhir_resource(resource_type):
    """ FHIR resource endpoint.
    """
    from researchapp.services.providers import provider_service

    if resource_type != 'Practitioner':
        raise Forbidden()

    def to_fhir(resource):  # pylint: disable=missing-docstring
        return {
            'resource': {
                'resourceType': 'Practitioner',
                'name': resource.name,
            }
        }

    practitioners = provider_service().filter_providers(**request.args)
    entries = [to_fhir(practitioner) for practitioner in practitioners]

    return jsonify({
        'resourceType': 'Bundle',
        'total': len(entries),
        'entries': entries,
    })
