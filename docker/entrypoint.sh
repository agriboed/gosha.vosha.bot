#!/usr/bin/env bash
set -e

echo 'Starting'

chmod 0777 -R /home/ubuntu/logs

/usr/bin/python3 /home/ubuntu/src/manage.py &>> /home/ubuntu/logs/debug.log &

echo 'Started'

tail -f /dev/null

exec "$@"