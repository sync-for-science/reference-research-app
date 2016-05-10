""" I'm a cli script """


USAGE_MESSAGE = 'Usage: {cmd} <config_uri>\n(example: "{cmd} development.ini")'


def console_config(route_func):
    """ Decorator  to bootstrap cli "routes". """

    def func_wrapper():
        """ Bootstrap the application, call the original method. """
        import os
        import sys
        from pyramid.paster import bootstrap

        argv = sys.argv
        if len(argv) != 2:
            cmd = os.path.basename(argv[0])
            print(USAGE_MESSAGE.format(cmd=cmd))
            sys.exit(1)

        config_uri = argv[1]
        env = bootstrap(config_uri)

        # call the original route method
        route_func(env['request'])

        env['closer']()

    return func_wrapper


@console_config
def fetch_participant_resources(request):  # pylint: disable=unused-argument
    """ For each participant/provider combo, download all their resources.
    """
    from researchapp.services.participants import participant_service
    from researchapp.services.providers import provider_service
    from researchapp.services.resources import resource_service
    import transaction

    with transaction.manager:
        participant = participant_service().get_participant('1551992')
        provider = provider_service().find_provider()

        resource_service().sync(participant, provider)


@console_config
def initialize_db(request):  # pylint: disable=unused-argument
    """ Initialize database tables, create a Participant record. """
    from researchapp.models import DBSession, Base, Participant, Provider
    import transaction

    Base.metadata.create_all(DBSession.get_bind())

    with transaction.manager:
        participant = Participant()
        DBSession.add(participant)

        provider = Provider(name="Dr. Smart",
                            city="Boston",
                            state="Massachusetts",
                            fhir_url="http://52.39.26.206:9000/api/fhir")
        DBSession.add(provider)

