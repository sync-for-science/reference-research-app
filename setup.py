import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires=['pyramid==1.6.1', 'pyramid_jinja2', 'jinja2','sqlalchemy', 'mysqlclient', 'waitress','pyramid_tm','pyramid_debugtoolbar','zope.sqlalchemy']

setup(name='ResearchApp',
      version='0.0',
      description='ResearchApp',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web pyramid pylons',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="researchapp",
      entry_points = """\
      [paste.app_factory]
      main = researchapp:main
      [console_scripts]
      initialize_researchapp_db = researchapp.initialize_db:main
      """,
      paster_plugins=['pyramid'],
      )
