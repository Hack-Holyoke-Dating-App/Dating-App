FROM python:2.7.15-stretch

# Setup Server
WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

CMD ./scripts/run.sh
