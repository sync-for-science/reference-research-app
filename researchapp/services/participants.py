""" Participants Service
"""
import json
import subprocess

from researchapp.extensions import db
from researchapp.models.participants import Participant, Authorization
from researchapp.services import oauth


def participant_service(which='db'):
    """ factory method """

    if which == 'file':
        return FileService()
    if which == 'db':
        return DbService(db.session)


class DbService(object):
    """ Database backed ParticipantService
    """

    def __init__(self, session):
        """ init """
        self._session = session

    def store_authorization(self, grant, practitioner):
        """ Stores an authorization """
        code = grant['code']

        token = oauth.code_to_token(code, practitioner)

        participant = self._session.\
            query(Participant).\
            filter_by(id=1).\
            one()

        authorization = Authorization(scope=token.get('scope'),
                                      access_token=token.get('access_token'),
                                      token_type=token.get('token_type'),
                                      client_id=token.get('client_id'),
                                      patient=token.get('patient'),
                                      refresh_token=token.get('refresh_token'),
                                      practitioner=practitioner)
        participant.authorizations.append(authorization)

        self._session.add(authorization)
        self._session.commit()

        # TODO: Something more robust than this to kick-start resource syncing
        subprocess.Popen(['./manage.py', 'fetch_participant_resources'])

    def get_participant(self, participant_id):  # pylint: disable=unused-argument
        """ Returns a single identified participant.

        Currently we ignore participant_id because there is only one.
        """
        participant = self._session.\
            query(Participant).\
            filter_by(id=participant_id).\
            one()

        return participant


class FileService(object):
    """ Local file backed Participant Service
    """

    def __init__(self):
        """ File backed provider service """
        self.patients = self._load_patients()

    def store_authorization(self, authorization, provider):
        """ Stores an authorization """
        code = authorization['code']

        token = oauth.code_to_token(code, provider)

        self.patients['1551992'] = token

        with open('patients.json', 'w+') as handle:
            json.dump(self.patients, handle)

    def get_participant(self, participant_id):
        """ Returns a single identified participant. """
        return self.patients[participant_id]

    def _load_patients(self):
        try:
            with open('patients.json') as handle:
                return json.load(handle)
        except FileNotFoundError:
            return {}
