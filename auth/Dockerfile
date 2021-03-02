from python:3.9

ENV PYTHONUNBUFFERED 1
ENV PROJECT_FOLDER=/usr/src/auth
# Database.
ENV DATABASE=postgres
ENV SQL_HOST=auth_db
ENV SQL_PORT=5432
# RabbitMQ.
ENV BROKER=rmq
ENV RMQ_HOST=rmq_server
ENV RMQ_PORT=5672
# File server.
ENV FILE_SERVER=samba
ENV SAMBA_HOST=192.168.0.44
ENV SAMBA_PORT=445
# Flask.
ENV FLASK_APP=server.py
ENV FLASK_DEBUG=1

# create the auth user
RUN addgroup --system auth && adduser --system --group auth

WORKDIR ${PROJECT_FOLDER}

COPY ./project ${PROJECT_FOLDER}/project/
COPY ./project/.env.dev ${PROJECT_FOLDER}/project/.env
COPY ./server.py ${PROJECT_FOLDER}
COPY ./entrypoint.sh ${PROJECT_FOLDER}
COPY requirements.txt ${PROJECT_FOLDER}/requirements.txt

RUN apt-get update && apt-get install -y netcat
RUN pip install -r ${PROJECT_FOLDER}/requirements.txt

RUN chown -R auth:auth ${PROJECT_FOLDER}
USER auth

# run entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
