import hashlib
import json
from base import app, api, Resource, Flask, request
import random

class RouteMonitoringResource(Resource):
    def get(self):
        r = random.random()
        if r > 0.9:
            data_md5 = hashlib.md5(json.dumps('error', sort_keys=True).encode('utf-8')).hexdigest()
        else:
            data_md5 = hashlib.md5(json.dumps(request.json, sort_keys=True).encode('utf-8')).hexdigest()
        
        return {"checksum": data_md5}, 200

api.add_resource(RouteMonitoringResource, '/health')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
