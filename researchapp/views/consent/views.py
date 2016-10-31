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
import requests

BP = Blueprint('consent', __name__, template_folder='templates')
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
    return redirect('http://tests.dev.syncfor.science:9005/providers/1/launch')


@BP.route('/authorized')
def authorized_callback():
    ''' Hand off the OAuth process.
    '''
    params = {
        'redirect_uri': request.url,
    }
    requests.post('http://tests.dev.syncfor.science:9005/participants/1/authorizations/1', data=params)

    return redirect(url_for('.connected'))


@BP.route('/connected')
def connected():
    ''' Show all connected providers.
    '''
    resp = requests.get('http://tests.dev.syncfor.science:9005/participants/1/authorizations')
    return render_template('connected.jinja2', authorizations=resp.json())


@BP.route('/api/providers')
def api_providers():
    ''' List providers.
    '''
    return jsonify([PROVIDER])
