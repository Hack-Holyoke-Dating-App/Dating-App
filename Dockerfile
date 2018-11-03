FROM python:2.7.15-stretch

WORKDIR /app

RUN pip install -r requirements.txt

CMD flask run
