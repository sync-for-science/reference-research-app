from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker,scoped_session

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

#Define your models here
#class MyModel(Base):
#    pass

def initialize_sql(engine):
    DBSession.configure(bind=engine)
    
