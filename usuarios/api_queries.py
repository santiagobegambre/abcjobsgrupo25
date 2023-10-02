import hashlib
import json
from base import app, api, Resource, Flask, request
import random

class RouteMonitoringResource(Resource):
    def get(self):
        return {"result": "Certificacion realizada correctamente"}, 200

api.add_resource(RouteMonitoringResource, '/cert')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', ssl_context='adhoc')
