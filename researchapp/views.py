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
    oauth_config = service.oauth_for_provider(provider)

    return {'provider': provider, 'oauth_config': oauth_config}


@view_config(route_name='connected', renderer='templates/connected.jinja2')
def view_connected(request):
    from researchapp.services.patients import patient_service
    from researchapp.services.fhir import get_patient

    service = patient_service()
    patient = service.refresh_authorization('1551992')

    fhir_patient = get_patient(patient)

    return {'patient': fhir_patient}


@view_config(route_name='authorized')
def authorized(request):
    from researchapp.services.patients import patient_service
    from pyramid.httpexceptions import HTTPFound

    service = patient_service()
    service.store_authorization(request.GET)

    url = request.route_url('connected')

    return HTTPFound(location=url)
