from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from collector.microsoft.api import Microsoft
from collector.zeev.api import Zeev
from main import DocumentManager

app = Flask(__name__)
CORS(app)
api = Api(app)

# Register routes
api.add_resource(Microsoft, '/api/microsoft/documents')
api.add_resource(Zeev, '/api/zeev/documents')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 