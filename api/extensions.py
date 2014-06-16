from flask_restful import Api
from flask_restful.utils import cors
from flask_pymongo import PyMongo

api_decorators = [cors.crossdomain('*')]
api = Api(decorators=api_decorators)
api.decorators
mongo = PyMongo()
