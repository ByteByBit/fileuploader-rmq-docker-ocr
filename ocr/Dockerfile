from python:3.9

ENV PYTHONUNBUFFERED 1
ENV PROJECT_FOLDER=/usr/src/ocr
# RabbitMQ.
ENV BROKER=rmq
ENV RMQ_HOST=rmq_server
ENV RMQ_PORT=5672
# File server.
ENV FILE_SERVER=samba
ENV SAMBA_HOST=192.168.0.44
ENV SAMBA_PORT=445

# Create the ocr user.
RUN addgroup --system ocr && adduser --system --group ocr

WORKDIR ${PROJECT_FOLDER}

COPY ./.env ${PROJECT_FOLDER}
COPY ./utils.py ${PROJECT_FOLDER}
COPY ./worker.py ${PROJECT_FOLDER}
COPY ./entrypoint.sh ${PROJECT_FOLDER}
COPY requirements.txt ${PROJECT_FOLDER}/requirements.txt

RUN apt-get update && apt-get install -y tesseract-ocr-dan && apt-get install -y netcat

RUN pip install -r ${PROJECT_FOLDER}/requirements.txt

RUN chown -R ocr:ocr ${PROJECT_FOLDER}

USER ocr

# run entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]