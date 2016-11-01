''' Define the routes in consent blueprint.
'''
from flask import (
    Blueprint,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)

from researchapp.extensions import sync

BP = Blueprint('consent', __name__, template_folder='templates')
PARTICIPANT = 1
PROVIDER = {
    'client-id': 'api-test',
    'id': 1,
    'name': 'smart',
}


@BP.route('/')
def index():
    ''' Show homepage.
    '''
    return render_template('index.jinja2')


@BP.route('/share-my-data')
def share_my_data():
    ''' Show "share my data" screen.
    '''
    return render_template('share_my_data.jinja2')


@BP.route('/consent')
def consent():
    ''' Show "consent" screen.
    '''
    return render_template('consent.jinja2', provider=PROVIDER)


@BP.route('/authorize')
def authorize():
    ''' Start the OAuth process.
    '''
    return redirect(sync.get_provider_launch_url(PROVIDER['id']))


@BP.route('/authorized')
def authorized_callback():
    ''' Hand off the OAuth process.
    '''
    sync.create_authorization(PROVIDER['id'], PARTICIPANT, request.url)

    return redirect(url_for('.connected'))


@BP.route('/connected')
def connected():
    ''' Show all connected providers.
    '''
    authorizations = sync.list_authorizations(PARTICIPANT)
    return render_template('connected.jinja2', authorizations=authorizations)


@BP.route('/api/providers')
def api_providers():
    ''' List providers.
    '''
    return jsonify(sync.list_providers())
