from python:3.9

ENV PYTHONUNBUFFERED 1
ENV PROJECT_FOLDER=/usr/src/preprocessor
# RabbitMQ.
ENV BROKER=rmq
ENV RMQ_HOST=rmq_server
ENV RMQ_PORT=5672
# File server.
ENV FILE_SERVER=samba
ENV SAMBA_HOST=192.168.0.44
ENV SAMBA_PORT=445

# Create the preprocessor user.
RUN addgroup --system preprocessor && adduser --system --group preprocessor

WORKDIR ${PROJECT_FOLDER}

COPY ./utils.py ${PROJECT_FOLDER}
COPY ./config.py ${PROJECT_FOLDER}
COPY ./worker.py ${PROJECT_FOLDER}
COPY ./entrypoint.sh ${PROJECT_FOLDER}
COPY ./.env.dev ${PROJECT_FOLDER}/.env
COPY requirements.txt ${PROJECT_FOLDER}/requirements.txt

RUN mkdir ${PROJECT_FOLDER}/tmp
# Update & install netcat.
RUN apt-get update && apt-get install -y netcat
# Install requirements.
RUN pip install -r ${PROJECT_FOLDER}/requirements.txt

# Set user the owner of project folder.
RUN chown -R preprocessor:preprocessor ${PROJECT_FOLDER}

USER preprocessor

# run entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]