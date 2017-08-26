#!/bin/bash

# Name of the application
NAME="blueswitch"

# Django project directory
DJANGODIR=/home/finoit/blueswitch

# The user to run as
USER=finoit

# The group to run as
GROUP=finoit

# How many worker processes should Gunicorn spawn
NUM_WORKERS=6

# Maximum number of requests a worker will process before restarting.
NUM_MAX_REQUEST=100

# Which settings file should Django use
DJANGO_SETTINGS_MODULE=config.settings

# WSGI module name
DJANGO_WSGI_MODULE=config.wsgi

# Access logs
ACCESS_LOG='/home/finoit/blueswitch/tmp/logs/access.log'

# Error logs --error-logfile $ERROR_LOG
ERROR_LOG='/home/finoit/blueswitch/tmp/logs/error.log'

# Log Level
LOG_LEVEL=debug # Options are debug, info, warning, error, critical

# Socket File to bind to
SOCKFILE=/home/finoit/blueswitch/tmp/sockets/gunicorn.sock

################################# END OF CONFIGURATIONS #################################


# ---------------------------------------------------------------------------------------

# Change to project directory
cd $DJANGODIR

# Activate the virtual environment
source env/bin/activate

# Activate project environment
export PYTHONPATH=$DJANGODIR:$PYTHONPATH
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec gunicorn $DJANGO_WSGI_MODULE:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --max-requests $NUM_MAX_REQUEST \
  --user=$USER --group=$GROUP \
  --log-level=$LOG_LEVEL \
  --bind=unix:$SOCKFILE \
  --access-logfile $ACCESS_LOG \
  --error-logfile $ERROR_LOG
