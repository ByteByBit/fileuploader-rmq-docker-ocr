#!/bin/sh
COUNT=0
NR_TO_REPORT=100
# Broker.
if [ "$BROKER" = "rmq" ];
then
    echo "Waiting for RabbitMQ broker."
    while ! nc -z $RMQ_HOST $RMQ_PORT; do
      COUNT=$((COUNT+1))
      sleep 1
      if [ $COUNT -gt $NR_TO_REPORT ]
      then
        echo "RabbitMQ broker unreachable."
        COUNT=0
      fi
    done
    echo "RabbitMQ broker up."
fi

exec "$@"

# Start consumer.
python3 "$PROJECT_FOLDER/worker.py"