""" Resources Service
"""
import json

from researchapp.extensions import db
from researchapp.models.resources import Resource
from researchapp.services import fhir


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


def resource_service(which='db'):
    """ factory method """
    if which == 'db':
        return DbService()


class DbService(object):
    """ Database backed ParticipantService
    """

    def __init__(self):
        pass

    def sync(self, participant):
        """ Sync, FOR SCIENCE!
        """
        for authorization in participant.authorizations:
            practitioner = authorization.practitioner

            self._sync_practitioner(participant, practitioner)

    def _sync_practitioner(self, participant, practitioner):
        """ Sync just one practitioner.
        """
        for ccds, endpoints in S4S_RESOURCES.items():
            for endpoint in endpoints:
                try:
                    bundle = fhir.query(participant, practitioner, endpoint)
                except AssertionError as err:
                    print(err, endpoint)
                    continue

                if not bundle:
                    continue

                for entry in bundle.get('entry', []):
                    self.save_resource(entry['resource'],
                                       participant,
                                       practitioner)

        resource = fhir.get_patient(participant, practitioner)
        if resource:
            self.save_resource(resource, participant, practitioner)
        db.session.commit()

    def save_resource(self, entry, participant, practitioner):
        """ Save a resource to the database.
        """
        try:
            resource = Resource(entry=json.dumps(entry),
                                fhir_id=entry.get('id', None),
                                fhir_resource_type=entry['resourceType'],
                                participant=participant,
                                practitioner=practitioner)
            db.session.add(resource)
        except KeyError as err:
            print(entry)
            raise

    def find_by_participant(self, participant):
        """ Get all the resources belonging to a single participant.
        """
        resources = db.session.query(Resource).\
            filter_by(participant=participant).\
            group_by(Resource.fhir_id).\
            all()

        return resources

    def find_all_for_participant(self, participant):
        """ Get all the authorizations and resources for a participant.
        """
        found = []

        for practitioner in participant.practitioners:
            resources = db.session.query(Resource).\
                filter_by(participant=participant).\
                filter_by(practitioner=practitioner).\
                group_by(Resource.fhir_id).\
                all()

            found.append({
                'resources': resources,
                'practitioner': practitioner,
            })

        return found
