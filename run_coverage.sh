#!/bin/bash
#source /usr/local/bin/virtualenvwrapper.sh
#workon nextbus
coverage run --source='.' manage.py test
coverage html