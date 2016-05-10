""" models """
from sqlalchemy import (
    Column,
    Integer,
    String,
)
from . import Base


class Provider(Base):
    """ Provider """
    __tablename__ = 'provider'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    city = Column(String)
    state = Column(String)
    fhir_url = Column(String)
