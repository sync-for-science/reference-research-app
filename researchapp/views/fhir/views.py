""" Some views"""
from flask import (
    jsonify,
    request,
)
from injector import inject
from werkzeug.exceptions import Forbidden

from researchapp.blueprints import fhir
from researchapp.services import providers


@fhir.route('/<resource_type>')
@inject(service=providers.ProviderService)
def fhir_resource(service, resource_type):
    """ FHIR resource endpoint.
    """
    if resource_type != 'Practitioner':
        raise Forbidden()

    def to_fhir(resource):  # pylint: disable=missing-docstring
        return {
            'resource': {
                'resourceType': 'Practitioner',
                'name': resource.name,
            }
        }

    query = {}
    if 'name' in request.args:
        query['name'] = request.args['name']
    practitioners = service.filter_providers(**query)
    entries = [to_fhir(practitioner) for practitioner in practitioners]

    return jsonify({
        'resourceType': 'Bundle',
        'total': len(entries),
        'entries': entries,
    })
