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
        assert len(providers) <= 1, 'Too many matched providers.'
        return render_template('consent.jinja2', provider=providers[0])
    except IndexError:
        return render_template('invalid_provider.jinja2')


@BP.route('/authorize', methods=['POST'])
def authorize():
    ''' Start the OAuth process.
    '''
    try:
        provider_id = request.form.get('provider')
        return redirect(sync.get_provider_launch_url(provider_id, PARTICIPANT))
    except KeyError:
        return render_template('invalid_provider.jinja2')


@BP.route('/authorized', , methods=['GET', 'POST'])
def authorized_callback():
    ''' Hand off the OAuth process.
    '''
    try:
        sync.create_authorization(PARTICIPANT, request.url)
        return redirect(url_for('.connected'))
    except (AssertionError, ValueError):
        return render_template('oauth_error.jinja2')
    except KeyError:
        return render_template('invalid_provider.jinja2')


@BP.route('/connected')
def connected():
    ''' Show all connected providers.
    '''
    try:
        authorizations = sync.list_authorizations(PARTICIPANT)
        authorizations = [authz for authz in authorizations
                          if authz['status'] == 'active']
        return render_template('connected.jinja2', authorizations=authorizations)
    except ValueError:
        return render_template('invalid_provider.jinja2')


@BP.route('/api/providers')
def api_providers():
    ''' List providers.
    '''
    return jsonify(sync.list_providers())
