FROM python:3.7-alpine

ENV FLASK_APP app

RUN adduser -D flask_app
USER flask_app

WORKDIR /home/flask_app

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt

COPY app app

COPY boot.sh ./

# run-time configuration
EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
