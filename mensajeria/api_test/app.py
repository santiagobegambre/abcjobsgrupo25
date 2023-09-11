from flask import Flask
from flask_cors import CORS
from flask_restful import Api, Resource
import os

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
            resp = {
                'connecting_ip': request.headers['X-Real-IP'],
                'proxy_ip': request.headers['X-Forwarded-For'],
                'host': request.headers['Host'],
                'user-agent': request.headers['User-Agent']
            }
            return jsonify(resp)
    
class FlaskHealthCheck(Resource):
      def get(self):
        return "success"

api.add_resource(HelloWorld, '/')
api.add_resource(FlaskHealthCheck, '/flask-health-check')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get("FLASK_SERVER_PORT"), debug=True)