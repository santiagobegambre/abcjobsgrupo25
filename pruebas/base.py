from flask import Flask, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)