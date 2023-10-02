from datetime import datetime, timedelta
from flask import Flask
from flask_jwt_extended import create_access_token
from flask_jwt_extended import JWTManager
from flask_restful import Api
import timesched
import requests
import hashlib
import json
import logging
import os

EXPERIMENTO_ID = os.environ.get("EXPERIMENTO_ID")

app = Flask(__name__)
api = Api(app)
output_file_path = f"output/{EXPERIMENTO_ID}.csv"

def write_to_output(message):
    print(message)
    with open(output_file_path, "a") as output_file:
        output_file.write(f"{message}\n")

s = timesched.Scheduler()
def callback(typ, arg):
    url = 'https://usuarios:5000/cert'
    headers = {
        'Content-Type': 'application/json'
    }
    body = {
        'id': 583969794,
        'name': 'monitor'
    }

    response = requests.get(url, verify=False, headers=headers, json=body)
    service_response = response.json()
    service_response = service_response['result']

    write_to_output(f'{service_response}')
callback('started', 'now')

minute = timedelta(minutes=0.5)
s.repeat(minute, 0, callback, 'repeat', minute)
s.run()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', ssl_context='adhoc')