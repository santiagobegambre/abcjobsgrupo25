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
logger = logging.getLogger(__name__)
logging.basicConfig(filename='record.log', level=logging.INFO)


app = Flask(__name__)
api = Api(app)
output_file_path = f"output/{EXPERIMENTO_ID}.csv"

def write_to_output(message):
    print(message)
    with open(output_file_path, "a") as output_file:
        output_file.write(f"{message}\n")

s = timesched.Scheduler()
write_to_output("time;response;expected;result")
def callback(typ, arg):
    ds = str(datetime.now())[:19]
    
    url = 'http://pruebas:5000/health'
    headers = {
        'Content-Type': 'application/json'
    }
    body = {
        'id': 583969794,
        'name': 'monitor'
    }
    
    response = requests.get(url, verify=False, headers=headers, json=body)
    md5_response = response.json()
    checksum = md5_response['checksum']

    data_md5 = hashlib.md5(json.dumps(body, sort_keys=True).encode('utf-8')).hexdigest()

    write_to_output(f'{datetime.now()};{data_md5};{checksum};{"ok"if(checksum==data_md5) else "fail"}')
    
    print(f'{ds} {typ} {arg}, active={s.count()}, response={response.text}, md5={data_md5}, md5={checksum}')

callback('started', 'now')

minute = timedelta(minutes=0.1)
s.repeat(minute, 0, callback, 'repeat', minute)
s.run()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')