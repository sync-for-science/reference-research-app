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
        return self.organization.url

    @property
    def client_id(self):
        return self.organization.oauth_client.client_id

    @property
    def client_secret(self):
        return self.organization.oauth_client.client_secret

    @property
    def scope(self):
        return self.organization.oauth_client.scope


class OAuthClient(Base):
    """ An oAuth Client.
    """
    __tablename__ = 'oauth_client'
    id = Column(Integer, primary_key=True)
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
    url = Column(String)

    oauth_client = orm.relationship('OAuthClient',
                                    back_populates='organization',
                                    uselist=False)
