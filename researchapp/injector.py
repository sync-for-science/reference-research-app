from flask_injector import FlaskInjector
from injector import Injector


class InjectorExtension(object):
    """
    """
    def __init__(self):
        self.injector = None
        self.modules = []

    def register(self, module):
        self.modules.append(module)

    def init_app(self, app):
        self.injector = Injector(self.modules)
        FlaskInjector(app=app, injector=self.injector)
