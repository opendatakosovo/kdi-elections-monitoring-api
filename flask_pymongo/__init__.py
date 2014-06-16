import pymongo
import pymongo.uri_parser
from flask import current_app

DEFAULT_CONFIG_PREFIX='MONGO_'
EXT_KEY = 'pymongo'

#delegation until code base does not use flask_pymongo.DESCENDING
DESCENDING=pymongo.DESCENDING
ASCENDING=pymongo.ASCENDING

class PyMongo(object):
    def __init__(self, app=None, config_prefix=DEFAULT_CONFIG_PREFIX):
        self.config_prefix = config_prefix
        if app is not None:
            self.init_app(app)

    def init_app(self, app, client=None):
        if client is None:
            mongo_uri = app.config[self.config_key_for_uri]
            parsed = pymongo.uri_parser.parse_uri(mongo_uri)
            options = parsed.get('options', {})
            ClientClass = pymongo.MongoReplicaSetClient if 'replicaset' in options else pymongo.MongoClient
            client = ClientClass(mongo_uri)

        if EXT_KEY not in app.extensions:
            app.extensions[EXT_KEY] = {}
        app.extensions[EXT_KEY][self.config_prefix] = client


    @property
    def config_key_for_uri(self):
        return self.config_prefix + 'URI'

    @property
    def db(self):
        return self.client.get_default_database()

    @property
    def client(self):
        return current_app.extensions[EXT_KEY][self.config_prefix]
