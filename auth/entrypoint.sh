#!/bin/sh
COUNT=0
NR_TO_REPORT=100
# Database.
if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for PostgreSQL."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      COUNT=$((COUNT+1))
      sleep 1

      if [ $COUNT -gt $NR_TO_REPORT ]
      then
        echo "PostgreSQL unreachable."
        COUNT=0
      fi
    done
    echo "PostgreSQL up."
fi
COUNT=0
# Broker.
if [ "$BROKER" = "rmq" ];
then
    echo "Waiting for RabbitMQ broker."
    while ! nc -z $SQL_HOST $SQL_PORT; do
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

flask run