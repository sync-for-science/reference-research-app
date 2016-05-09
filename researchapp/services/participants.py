""" Participants Service
"""
import json
from researchapp.models import DBSession
from researchapp.models.participants import Participant, Authorization


def participant_service(which='db'):
    """ factory method """
    if which == 'file':
        return FileService()
    if which == 'db':
        return DbService()


class DbService(object):
    """ Database backed ParticipantService
    """

    def __init__(self):
        """ init """

    def store_authorization(self, grant, provider):
        """ Stores an authorization """
        from researchapp.services import oauth
        code = grant['code']

        token = oauth.code_to_token(code, provider)

        participant = DBSession.\
            query(Participant).\
            filter_by(id=1).\
            one()
        authorization = Authorization(scope=token['scope'],
                                      access_token=token['access_token'],
                                      token_type=token['token_type'],
                                      client_id=token['client_id'],
                                      patient=token['patient'],
                                      refresh_token=token['refresh_token'])
        participant.authorizations.append(authorization)

        DBSession.add(authorization)

    def get_participant(self, participant_id):  # pylint: disable=unused-argument
        """ Returns a single identified participant.

        Currently we ignore participant_id because there is only one.
        """
        participant = DBSession.\
            query(Participant).\
            filter_by(id=1).\
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
        from researchapp.services import oauth
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
