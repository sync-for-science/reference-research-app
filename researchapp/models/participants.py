""" Participants

Participants are the prototypical "users" of this application.
"""
from sqlalchemy import (
    ForeignKey,
    Column,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from researchapp.extensions import db


PARTICIPANT_AUTHORIZATION = db.Table(
    'participant_authorization',
    Column('participant_id', ForeignKey('participant.id'), primary_key=True),
    Column('authorization_id', ForeignKey('authorization.id'), primary_key=True)
)
THE_ONLY_PARTICIPANT_ID = 1


class Participant(db.Model):
    """ Participant """
    __tablename__ = 'participant'
    id = Column(Integer, primary_key=True)

    # one to many Participant->Authorization
    authorizations = relationship('Authorization',
                                  secondary=PARTICIPANT_AUTHORIZATION)

    @property
    def practitioners(self):
        """ All the Practitioners for this patient.

        Collapses all the authorizations into a list of unique Practitioners.
        """
        practitioners = set()
        for authz in self.authorizations:
            practitioners.add(authz.practitioner)

        return practitioners

    def authorization(self, practitioner):
        """ We want the most recent authorization.
        """
        authorizations = [authz for authz in self.authorizations
                          if authz.practitioner == practitioner]
        try:
            return authorizations[-1]
        except IndexError:
            return None


class Authorization(db.Model):
    """ Authorization """
    __tablename__ = 'authorization'
    id = Column(Integer, primary_key=True)
    fhirclient = Column(String)

    # many to one Authorization -> Practitioner
    practitioner_id = Column(Integer, ForeignKey('practitioner.id'))
    practitioner = relationship('Practitioner')
