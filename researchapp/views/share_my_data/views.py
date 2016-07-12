""" Some views"""
from flask import (
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.exceptions import Forbidden

from researchapp.blueprints import share_my_data


@share_my_data.route('/')
def view_index():
    """ Homepage.
    """
    return render_template('home.jinja2', project='ResearchApp')


@share_my_data.route('/share-my-data')
def view_share_my_data():
    """ Share my data.
    """
    from researchapp.services.providers import provider_service

    service = provider_service()
    providers = service.filter_providers()

    return render_template('share_my_data.jinja2', providers=providers)


@share_my_data.route('/consent')
def view_consent():
    """ Consent page.
    """
    from researchapp.services.providers import provider_service
    from researchapp.services import fhir, oauth
    import uuid

    service = provider_service()
    practitioner = service.find_provider(name=request.args['doctor'])

    # set a new "state" token
    session['state'] = str(uuid.uuid4())
    session['practitioner_id'] = practitioner.id

    view_data = {
        'practitioner': practitioner,
        'authorize_url': fhir.get_oauth_uris(practitioner)['authorize'],
        'state': session['state'],
        'redirect_uri': oauth.redirect_uri(),
        'client_id': practitioner.client_id,
    }

    return render_template('consent.jinja2', **view_data)


@share_my_data.route('/connected')
def view_connected():
    """ Show all connected providers.
    """
    from researchapp.services.participants import participant_service
    from researchapp.services.providers import provider_service
    from researchapp.services.resources import resource_service

    participant = participant_service().get_participant(1)
    connections = resource_service().find_all_for_participant(participant)

    return render_template('connected.jinja2', connections=connections)


@share_my_data.route('/authorized')
def authorized():
    """ Handle authorized callback.
    """
    from researchapp.services.participants import participant_service
    from researchapp.services.providers import provider_service

    # make sure that "state" is what we provided
    if request.args['state'] != session['state']:
        raise Forbidden()

    # state tokens should only be used once
    session['state'] = None
    practitioner_id = session['practitioner_id']

    practitioner = provider_service().find_provider(id=practitioner_id)
    participant_service().store_authorization(request.args, practitioner)

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
