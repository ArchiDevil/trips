FROM python:3.10-alpine AS application

COPY ./app/requirements.txt /requirements.txt
RUN python -m pip install -r /requirements.txt

COPY ./app/organizer /organizer
COPY ./app/alembic /alembic
COPY ./app/alembic.ini /alembic.ini

EXPOSE 8000

CMD ["gunicorn", "-b", "0.0.0.0:8000", "--workers=4", "organizer.wsgi:app", "--log-file", "-"]
