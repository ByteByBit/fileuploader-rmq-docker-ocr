from python:3.9

ENV PYTHONUNBUFFERED 1
ENV PROJECT_FOLDER=/usr/src/uploader_api
# Database.
ENV DATABASE=postgres
ENV SQL_HOST=upload_db
ENV SQL_PORT=5432
# RabbitMQ.
ENV BROKER=rmq
ENV RMQ_HOST=rmq_server
ENV RMQ_PORT=5672
# File server.
ENV FILE_SERVER=samba
ENV SAMBA_HOST=192.168.0.44
ENV SAMBA_PORT=445
# Auth container.
ENV AUTH=auth
ENV AUTH_HOST=auth
ENV AUTH_PORT=5000
ENV AUTH_URI=http://auth:5000/auth

# Create the uploader user.
RUN addgroup --system uploader && adduser --system --group uploader

WORKDIR ${PROJECT_FOLDER}

COPY ./project ${PROJECT_FOLDER}/project/
COPY ./project/.env.dev ${PROJECT_FOLDER}/project/.env
COPY ./server.py ${PROJECT_FOLDER}
COPY ./entrypoint.sh ${PROJECT_FOLDER}
COPY requirements.txt ${PROJECT_FOLDER}/requirements.txt

RUN mkdir ${PROJECT_FOLDER}/tmp

# Update & install netcat.
RUN apt-get update && apt-get install -y netcat
# Install requirements.
RUN pip install -r ${PROJECT_FOLDER}/requirements.txt

# Set user the owner of project folder.
RUN chown -R uploader:uploader ${PROJECT_FOLDER}

USER uploader

# run entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
