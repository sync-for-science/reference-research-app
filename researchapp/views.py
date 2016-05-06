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

    service = provider_service()
    provider = service.find_provider(name=request.GET['doctor'])

    return {'provider': provider}


@view_config(route_name='connected', renderer='templates/connected.jinja2')
def view_connected(request):
    from researchapp.services.participants import participant_service
    from researchapp.services.providers import provider_service
    from researchapp.services.fhir import get_patient

    participant = participant_service().get_participant('1551992')
    provider = provider_service().find_provider()

    patient = get_patient(participant, provider)

    return {'patient': patient}


@view_config(route_name='authorized')
def authorized(request):
    from researchapp.services.participants import participant_service
    from researchapp.services.providers import provider_service
    from pyramid.httpexceptions import HTTPFound

    provider = provider_service().find_provider()
    participant_service().store_authorization(request.GET, provider)

    url = request.route_url('connected')

    return HTTPFound(location=url)
