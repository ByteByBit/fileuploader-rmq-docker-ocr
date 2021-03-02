#!/bin/sh
NR_TO_REPORT=100
COUNT=0
echo "Samba fileserver entrypoint."
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
echo "RMQ broker entrypoint."
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

exec "$@"

python3 "$PROJECT_FOLDER/worker.py"
