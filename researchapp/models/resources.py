""" Resources

Resources are FHIR resources that we've downloaded and stored.
"""
import datetime

from sqlalchemy import (
    ForeignKey,
    Column,
    Integer,
    String,
    DateTime,
)
from sqlalchemy.orm import relationship

from researchapp.extensions import db


class Resource(db.Model):
    """ Resource """
    __tablename__ = 'resource'
    id = Column(Integer, primary_key=True)
    entry = Column(String)
    created = Column(DateTime, default=datetime.datetime.utcnow)

    fhir_id = Column(String)
    fhir_resource_type = Column(String)

    participant_id = Column(Integer, ForeignKey('participant.id'))
    participant = relationship('Participant')

    practitioner_id = Column(Integer, ForeignKey('practitioner.id'))
    practitioner = relationship('Practitioner')
