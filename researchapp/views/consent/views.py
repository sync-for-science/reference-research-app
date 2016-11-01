''' Define the routes in consent blueprint.
'''
from flask import (
    Blueprint,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from researchapp.extensions import sync

BP = Blueprint('consent', __name__, template_folder='templates')
PARTICIPANT = 1


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
    provider_id = request.args.get('doctor')
    providers = [provider for provider in sync.list_providers()
                 if str(provider['id']) == str(provider_id)]

    try:
        session['provider'] = providers[0]
        return render_template('consent.jinja2', provider=providers[0])
    except IndexError:
        return render_template('invalid_provider.jinja2')


@BP.route('/authorize', methods=['POST'])
def authorize():
    ''' Start the OAuth process.
    '''
    try:
        provider = session['provider']
        return redirect(sync.get_provider_launch_url(provider['id']))
    except KeyError:
        return render_template('invalid_provider.jinja2')


@BP.route('/authorized')
def authorized_callback():
    ''' Hand off the OAuth process.
    '''
    try:
        provider = session.pop('provider')
        sync.create_authorization(provider['id'], PARTICIPANT, request.url)

        return redirect(url_for('.connected'))
    except KeyError:
        return render_template('invalid_provider.jinja2')


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
