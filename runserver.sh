#!/bin/bash

pip install -r requirements.txt
service cron start
pserve development.ini --reload
