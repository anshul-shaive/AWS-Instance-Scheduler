#!/bin/sh
source venv/bin/activate

while true; do
    flask run --host='0.0.0.0'
    if [[ "$?" == "0" ]]; then
        break
    fi
    echo run command failed, retrying in 5 secs...
    sleep 5
done

exec gunicorn -b :5000 --access-logfile - --error-logfile - app
