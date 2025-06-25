#!/bin/bash
# migrate database
alembic upgrade head

# then run the app
exec gunicorn organizer.wsgi:app -b 0.0.0.0:8000 --workers=4 --access-logfile=- --error-logfile=-
