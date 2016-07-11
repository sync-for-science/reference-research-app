""" Authorize Service module.
"""
import json

from fhirclient import client
from flask import session
from flask_sqlalchemy import SQLAlchemy
from injector import inject

from researchapp.models.participants import (
    THE_ONLY_PARTICIPANT_ID,
    Authorization,
    Participant,
)
from researchapp.models.providers import Practitioner
from researchapp.services import oauth


class AuthorizeService(object):
    """ The service.
    """
    @inject(db=SQLAlchemy)
    def __init__(self, db):
        self._db = db

    def display_consent(self, practitioner_name):
        """ Everything we need to display a consent page.
        """
        practitioner = self._db.session.query(Practitioner).\
            filter_by(name=practitioner_name).\
            one()

        settings = {
            'app_id': practitioner.client_id,
            'app_secret': practitioner.client_secret,
            'api_base': practitioner.fhir_url,
            'redirect_uri': oauth.redirect_uri(),
            'scope': practitioner.scope,
        }
        fhir = client.FHIRClient(settings=settings)
        # Build an authorize_url *before* we save the state
        authorize_url = fhir.authorize_url

        session['practitioner_id'] = practitioner.id
        session['fhirclient'] = fhir.state

        return {
            'practitioner': practitioner.name,
            'authorize_url': authorize_url,
        }

    def register_authorization(self, callback_url):
        """ Validate and store a completed authorizations.
        """
        participant = self._db.session.query(Participant).\
            get(THE_ONLY_PARTICIPANT_ID)
        practitioner = self._db.session.query(Practitioner).\
            get(session['practitioner_id'])

        try:
            state = session['fhirclient']
            print(state)
            print(callback_url)
            fhir = client.FHIRClient(state=state)
            fhir.handle_callback(callback_url)
        except client.FHIRUnauthorizedException:
            raise FHIRUnauthorizedException()

        authorization = Authorization(fhirclient=json.dumps(fhir.state),
                                      practitioner=practitioner)
        participant.authorizations.append(authorization)

        self._db.session.add(authorization)
        self._db.session.commit()


class FHIRUnauthorizedException(Exception):
    """ FHIR Authorization failed.
    """


def configure(binder):
    """ Configure this module for the Injector.
    """
    binder.bind(AuthorizeService)
