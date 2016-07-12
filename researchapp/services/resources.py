""" Resources Service
"""
import json
import logging

from fhirclient import client
from fhirclient.models.fhirabstractbase import FHIRValidationError
from fhirclient.models.fhirelementfactory import FHIRElementFactory
from flask_sqlalchemy import SQLAlchemy
from injector import inject

from researchapp.models.participants import Participant
from researchapp.models.resources import Resource


S4S_RESOURCES = {
    'Smoking status': [
        'Observation?category=social-history&patient={patientId}',
    ],
    'Problems': [
        'Condition?patient={patientId}',
    ],
    'Medications and allergies': [
        'MedicationOrder?patient={patientId}',
        'MedicationStatement?patient={patientId}',
        'MedicationDispense?patient={patientId}',
        'MedicationAdministration?patient={patientId}',
        'AllergyIntolerance?patient={patientId}',
    ],
    'Lab results': [
        'Observation?category=laboratory&patient={patientId}',
    ],
    'Vital signs': [
        'Observation?category=vital-signs&patient={patientId}',
    ],
    'Procedures': [
        'Procedure?patient={patientId}',
    ],
    'Immunizations': [
        'Immunization?patient={patientId}',
    ],
    'Patient documents': [
        'DocumentReference?patient={patientId}',
    ],
}


class ResourceService(object):
    """ The service.
    """
    @inject(db=SQLAlchemy)
    def __init__(self, db):
        self._db = db

    def sync_participant(self, participant_id):
        """ Fetch all the resources for a given Participant.
        """
        participant = self._db.session.query(Participant).\
            get(participant_id)

        for authorization in participant.authorizations:
            self.sync_authorization(participant, authorization)

    def sync_authorization(self, participant, authorization):
        """ Fetch all the resources for a given authorization.
        """
        state = json.loads(authorization.fhirclient)
        fhir = client.FHIRClient(state=state)
        factory = ResourceFactory(participant, authorization.practitioner)

        try:
            patient = fhir.patient
            resource = factory.from_fhirclient_model(patient)
            self._db.session.add(resource)

            for ccds, endpoints in S4S_RESOURCES.items():
                logging.info('Begin import: %s', ccds)
                for endpoint in endpoints:
                    path = endpoint.format(patientId=patient.id)
                    bundle = fhir.server.request_json(path)
                    self.sync_bundle(bundle, factory)
        finally:
            state = json.dumps(fhir.state)
            authorization.fhirclient = state
            self._db.session.add(authorization)
            self._db.session.commit()

    def sync_bundle(self, bundle, factory):
        """ Save all the resources for a single bundle.
        """
        for entry in bundle.get('entry', []):
            try:
                resource = factory.from_dictionary(entry.get('resource'))
                self._db.session.add(resource)
            except FHIRValidationError:
                continue

    def display_connections(self, participant_id):
        """ Show all the connections stored for a participant.
        """
        participant = self._db.session.query(Participant).\
            get(participant_id)
        found = []

        for practitioner in participant.practitioners:
            resources = self._db.session.query(Resource).\
                filter_by(participant=participant).\
                filter_by(practitioner=practitioner).\
                group_by(Resource.fhir_id).\
                all()
            found.append({
                'resources': resources,
                'practitioner': practitioner,
            })

        return found


class ResourceFactory(object):
    """ Easy way to create Resources.
    """
    def __init__(self, participant, practitioner):
        self.participant = participant
        self.practitioner = practitioner

    def from_fhirclient_model(self, resource):
        """ Converts a fhirclient model to a Resource.
        """
        return Resource(entry=json.dumps(resource.as_json()),
                        fhir_id=resource.id,
                        fhir_resource_type=resource.resource_name,
                        participant=self.participant,
                        practitioner=self.practitioner)

    def from_dictionary(self, raw):
        """ Converts a dictionary to a Resource.
        """
        resource = FHIRElementFactory.instantiate(raw['resourceType'],
                                                  raw)
        return self.from_fhirclient_model(resource)


def configure(binder):
    """ Configure this module for the Injector.
    """
    binder.bind(ResourceService)
