FROM python:3.10 AS application

RUN apt update && apt install -y dos2unix

WORKDIR /app

COPY ./app/wait-for-it.sh /app/wait-for-it.sh
COPY ./app/run.sh /app/run.sh

COPY ./app/requirements.txt /app/requirements.txt
RUN python -m pip install -r /app/requirements.txt

COPY ./app/alembic /app/alembic
COPY ./app/alembic.ini /app/alembic.ini
COPY ./app/organizer /app/organizer

RUN dos2unix /app/wait-for-it.sh
RUN dos2unix /app/run.sh

EXPOSE 8000

CMD ["/bin/bash", "/app/run.sh"]
