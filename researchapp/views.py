# pylint: disable=unused-argument,missing-docstring
""" Some views"""
import json

from pyramid.i18n import TranslationStringFactory
from pyramid.view import view_config


_ = TranslationStringFactory('ResearchApp')


def prettify_json(json_str):
    data = json.loads(json_str)
    return json.dumps(data, indent=4)


@view_config(route_name='home', renderer='templates/home.jinja2')
def home(request):
    """ Homepage """
    return {'project': 'ResearchApp'}


@view_config(route_name='share_my_data',
             renderer='templates/share_my_data.jinja2')
def view_share_my_data(request):
    """ Share my data """
    from researchapp.services.providers import provider_service

    service = provider_service()
    providers = service.filter_providers()

    return {'providers': providers}


@view_config(route_name='consent', renderer='templates/consent.jinja2')
def view_consent(request):
    from researchapp.services.providers import provider_service
    from researchapp.services import fhir, oauth
    import uuid

    service = provider_service()
    practitioner = service.find_provider(name=request.GET['doctor'])

    # set a new "state" token
    request.session['state'] = str(uuid.uuid4())
    request.session['practitioner_id'] = practitioner.id

    return {
        'practitioner': practitioner,
        'authorize_url': fhir.get_oauth_uris(practitioner)['authorize'],
        'state': request.session['state'],
        'redirect_uri': oauth.redirect_uri(),
        'client_id': practitioner.client_id,
    }


@view_config(route_name='connected', renderer='templates/connected.jinja2')
def view_connected(request):
    from researchapp.services.participants import participant_service
    from researchapp.services.providers import provider_service
    from researchapp.services.resources import resource_service

    participant = participant_service().get_participant(1)

    return {
        'connections': resource_service().find_all_for_participant(participant)
    }


@view_config(route_name='authorized')
def authorized(request):
    from researchapp.services.participants import participant_service
    from researchapp.services.providers import provider_service
    from pyramid.httpexceptions import HTTPFound, HTTPForbidden

    # make sure that "state" is what we provided
    if request.GET['state'] != request.session['state']:
        raise HTTPForbidden()

    # state tokens should only be used once
    request.session['state'] = None
    practitioner_id = request.session['practitioner_id']

    practitioner = provider_service().find_provider(id=practitioner_id)
    participant_service().store_authorization(request.GET, practitioner)

    url = request.route_url('connected')

    return HTTPFound(location=url)


@view_config(route_name='fhir', renderer='json')
def fhir_resource(request):
    from researchapp.services.providers import provider_service
    from pyramid.httpexceptions import HTTPForbidden

    if request.matchdict['resourceType'] != 'Practitioner':
        raise HTTPForbidden()

    def to_fhir(resource):
        return {
            'resource': {
                'resourceType': 'Practitioner',
                'name': resource.name,
            }
        }

    practitioners = provider_service().filter_providers(**request.GET)
    entries = [to_fhir(practitioner) for practitioner in practitioners]

    return {
        'resourceType': 'Bundle',
        'total': len(entries),
        'entries': entries,
    }
