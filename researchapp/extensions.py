''' Any flask extensions go here.
'''
from flask_sqlalchemy import SQLAlchemy

from researchapp.sync_api import SyncExtension

db = SQLAlchemy()
sync = SyncExtension()
