#!/bin/sh
COUNT=0
NR_TO_REPORT=100
if [ "$DATABASE" = "postgres" ];
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
if [ "$FILE_SERVER" = "samba" ];
then
    echo "Waiting for Samba fileserver."

    while ! nc -z $SAMBA_HOST $SAMBA_PORT; do
      COUNT=$((COUNT+1))
      sleep 1

      if [ $COUNT -gt $NR_TO_REPORT ]
      then
        echo "Samba fileserver unreachable."
        COUNT=0
      fi

    done

    echo "Samba fileserver up."
fi

COUNT=0
if [ "$BROKER" = "rmq" ];
then
    echo "Waiting for RMQ broker."

    while ! nc -z $RMQ_HOST $RMQ_PORT; do
      COUNT=$((COUNT+1))
      sleep 1

      if [ $COUNT -gt $NR_TO_REPORT ]
      then
        echo "RMQ broker unreachable."
        COUNT=0
      fi

    done

    echo "RMQ broker up."
fi

COUNT=0
if [ "$AUTH" = "auth" ];
then
    echo "Waiting for auth container."

    while ! nc -z $AUTH_HOST $AUTH_PORT; do
      COUNT=$((COUNT+1))
      sleep 1

      if [ $COUNT -gt $NR_TO_REPORT ]
      then
        echo "Container auth unreachable."
        COUNT=0
      fi

    done

    echo "Container auth up."
fi

exec "$@"

echo 'Starting flask.'
flask run