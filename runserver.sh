#!/bin/sh

initialize_db development.ini
supervisorctl start after:*
