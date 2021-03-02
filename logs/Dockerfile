from python:3.9

ENV PYTHONUNBUFFERED 1
ENV PROJECT_FOLDER=/usr/src/logger
# RabbitMQ.
ENV BROKER=rmq
ENV RMQ_HOST=rmq_server
ENV RMQ_PORT=5672

# Create the logger user.
RUN addgroup --system logger && adduser --system --group logger

WORKDIR ${PROJECT_FOLDER}

COPY ./worker.py ${PROJECT_FOLDER}
COPY ./config.py ${PROJECT_FOLDER}
COPY ./logging.conf ${PROJECT_FOLDER}
COPY ./.env.dev ${PROJECT_FOLDER}/.env
COPY ./entrypoint.sh ${PROJECT_FOLDER}
COPY requirements.txt ${PROJECT_FOLDER}/requirements.txt

# Update & install netcat.
RUN apt-get update && apt-get install -y netcat
# Install requirements.
RUN pip install -r ${PROJECT_FOLDER}/requirements.txt

# Set user the owner of project folder.
RUN chown -R logger:logger ${PROJECT_FOLDER}

USER logger

# run entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]