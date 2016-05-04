from pyramid.i18n import TranslationStringFactory
from pyramid.view import view_config
from researchapp.models import DBSession


_ = TranslationStringFactory('ResearchApp')

@view_config(route_name='home', renderer='templates/home.jinja2')
def view_home(request):
    session = DBSession()
    #Use session to make queries
    #session.query()
    return {'project':'ResearchApp'}

@view_config(route_name='share_my_data', renderer='templates/share_my_data.jinja2')
def view_share_my_data(request):
    return {'project': 'ResearchApp'}

@view_config(route_name='consent', renderer='templates/consent.jinja2')
def view_consent(request):
    return {'project': 'ResearchApp'}

@view_config(route_name='connected', renderer='templates/connected.jinja2')
def view_connected(request):
    return {'project': 'ResearchApp'}
