# pylint: disable=invalid-name
""" All Flask blueprints for the entire application.

All blueprints for all views go here.
They shall be imported by the views themselves and by application.py.
Blueprint URL paths are defined here as well.
"""
from flask import Blueprint


def _factory(partial_module_string, url_prefix):
    """Generates blueprint objects for view modules.

    Args:
        partial_module_string (string): a view module without the absolute path
            (e.g. 'home.index' for researchapp.views.home.index).
        url_prefix: URL prefix passed to the blueprint.

    Returns:
        Blueprint instance for a view module.
    """
    name = partial_module_string
    import_name = 'researchapp.views.{0}'.format(partial_module_string)
    template_folder = 'templates'
    blueprint = Blueprint(name,
                          import_name,
                          template_folder=template_folder,
                          url_prefix=url_prefix)

    return blueprint


share_my_data = _factory('share_my_data.views', '')
fhir = _factory('fhir.views', '/fhir')


all_blueprints = (share_my_data, fhir,)
