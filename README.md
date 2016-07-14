# S4S Demo Research App

Demo for the Patient/Participant "Share my data" workflow

## Installation

```
pip install -r requirements.txt
```

## Running the app

```
./manage.py devserver
```

## Running the testso

To test the reference research app, use py.test.

```
pip install -e . # Install "researchapp" so that the tests can find it
py.test
```

To see the test coverage, generate a coverage report and navigate to /static/coverage/index.html.

```
py.test --cov=researchapp --cov-report html
```
