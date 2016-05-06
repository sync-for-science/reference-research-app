""" Patients Service
"""
import json


def patient_service(which='file'):
    """ factory method """
    if which == 'file':
        return FileService()


class FileService(object):
    """ Local file backed Patient Service
    """

    def __init__(self):
        """ File backed provider service """
        self.patients = self._load_patients()

    def store_authorization(self, authorization):
        """ Stores an authorization """
        from researchapp.services import oauth
        code = authorization['code']

        token = oauth.code_to_token(code)

        self.patients['1551992'] = token

        with open('patients.json', 'w+') as handle:
            json.dump(self.patients, handle)

    def refresh_authorization(self, patient):
        """ refresh """
        from researchapp.services import oauth
        patient = self.patients[patient]
        auth = oauth.refresh(patient['refresh_token'])

        return auth

    def _load_patients(self):
        try:
            with open('patients.json') as handle:
                return json.load(handle)
        except FileNotFoundError:
            return {}
