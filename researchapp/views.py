# pylint: disable=unused-argument,missing-docstring
""" Some views"""
from pyramid.i18n import TranslationStringFactory
from pyramid.view import view_config


_ = TranslationStringFactory('ResearchApp')


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
    from researchapp.services import fhir
    import uuid

    service = provider_service()
    provider = service.find_provider(name=request.GET['doctor'])

    # set a new "state" token
    request.session['state'] = str(uuid.uuid4())

    return {
        'provider': provider,
        'authorize_url': fhir.get_oauth_uris(provider)['authorize'],
        'state': request.session['state']
    }


@view_config(route_name='connected', renderer='templates/connected.jinja2')
def view_connected(request):
    from researchapp.services.participants import participant_service
    from researchapp.services.providers import provider_service
    from researchapp.services.resources import resource_service
    from researchapp.services.fhir import get_patient

    participant = participant_service().get_participant('1551992')

    resources = resource_service().find_by_participant(participant)

    return {'resources': resources}


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

    provider = provider_service().find_provider()
    participant_service().store_authorization(request.GET, provider)

    url = request.route_url('connected')

    return HTTPFound(location=url)
