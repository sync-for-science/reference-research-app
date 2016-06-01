""" models """
from sqlalchemy import (
    ForeignKey,
    Column,
    Integer,
    String,
    orm,
)
from . import Base


class Practitioner(Base):
    """ A Practitioner.
    """
    __tablename__ = 'practitioner'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    organization_id = Column(String, ForeignKey('organization.id'))
    organization = orm.relationship('Organization')

    @property
    def fhir_url(self):
        return self.organization.api.url

    @property
    def client_id(self):
        return self.organization.api.client_id

    @property
    def client_secret(self):
        return self.organization.api.client_secret

    @property
    def scope(self):
        return self.organization.api.scope


class Api(Base):
    """ A FHIR Api.
    """
    __tablename__ = 'api'
    id = Column(Integer, primary_key=True)
    url = Column(String)
    client_id = Column(String)
    client_secret = Column(String)
    scope = Column(String)

    organization_id = Column(String, ForeignKey('organization.id'))
    organization = orm.relationship('Organization')


class Organization(Base):
    """ An Organization.
    """
    __tablename__ = 'organization'
    id = Column(String, primary_key=True)
    name = Column(String)

    api = orm.relationship('Api', back_populates='organization', uselist=False)
