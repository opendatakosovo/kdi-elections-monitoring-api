import os
import logging

from flask import Flask, request
from .extensions import mongo, api

from .utils import FullModuleNameFormatter

def create_app(mongodb_client=None, **configs):
	''' Create and return the app instance.
	param mongodb_client:
	'''
	# init flask app and api
	app = Flask(__name__)
	
	#config
	app.config.from_object('api.settings')
	#app.config.from_pyfile('settings_local.py', silent=True)
	#app.config.from_envvar('FIVEPOINTS_SETTINGS', silent=True)
	app.config.update(configs)
	#logger
	configure_logging(app)
	
	#db
	mongo.init_app(app, mongodb_client)
	with app.app_context():
		app.logger.info('mongodb: %s', mongo.client)
		#for db, collIndexes in app.config['MONGO_INDEX_SPEC'].iteritems():
			#app.logger.info('ensuring mongodb indexes for db %s: collection %s' % (db, collIndexes))
			#mongo_ensure_index(mongo.client[db], collIndexes)
			
	#views stuff
	#app.url_value_preprocessor(url_preprocessor)
	#registering views must happen before api.init_app
	register_resources(api)
	api.init_app(app)
	
	return app

def configure_logging(app):
	''' Configure logging.
	:param app: The application instance.
	'''
	
	log_path = app.config['LOG_PATH']
	log_dir = os.path.dirname(log_path)
	if not os.path.exists(log_dir):
		os.makedirs(log_dir)
		
	log_level = getattr(logging, app.config['LOG_LEVEL'].upper())
	
	formatter = FullModuleNameFormatter('%(asctime)s %(levelname)s %(message)s [%(modulepath)s:%(lineno)d]')
	file_handler = logging.handlers.TimedRotatingFileHandler(log_path, when='midnight', interval=1, backupCount=365)
	file_handler.setFormatter(formatter)
	file_handler.setLevel(log_level)
	
	app.logger.addHandler(file_handler)
	app.logger.setLevel(log_level)
	app.logger.info('logging to: %s', log_path)

from .views.pollingstation import PollingStation

def register_resources(api):
	''' Register REST resources.
	:param api:
	'''
	api.add_resource(PollingStation,
		'/kdi/2014/generalelections/pollingstations',
		'/kdi/2014/generalelections/pollingstations/<string:commune>',
		'/kdi/2014/generalelections/pollingstations/<string:commune>/<string:city>',
		'/kdi/2014/generalelections/pollingstations/<string:commune>/<string:city>/<string:name>/')

