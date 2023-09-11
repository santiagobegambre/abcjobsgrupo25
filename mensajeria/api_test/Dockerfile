FROM python:3.8-slim

# layer caching for faster builds
COPY requirements.txt /
RUN pip install -r /requirements.txt

ADD . /api_test
WORKDIR /api_test

EXPOSE 5000

ENV FLASK_ENV=development0
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development

CMD flask run