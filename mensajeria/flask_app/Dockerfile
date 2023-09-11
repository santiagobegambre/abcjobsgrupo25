FROM python:3.8-slim

# layer caching for faster builds
COPY requirements.txt /
RUN pip install -r /requirements.txt

#COPY app.py /app.py
ADD . /flask_app
WORKDIR /flask_app

EXPOSE 5000

ENV FLASK_ENV=development
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development

CMD flask run


#CMD gunicorn --workers $WORKERS \
#  --threads $THREADS \
#  --bind 0.0.0.0:$PORT_APP \
#  --log-level DEBUG \
#  app:app