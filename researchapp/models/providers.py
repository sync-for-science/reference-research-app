""" models """
from sqlalchemy import (
    Column,
    Integer,
)
from . import Base


class Provider(Base):
    """ Provider """
    __tablename__ = 'provider'
    id = Column(Integer, primary_key=True)
