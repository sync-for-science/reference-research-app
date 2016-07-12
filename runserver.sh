#!/bin/sh

./manage.py initialize_db
supervisorctl start after:*
