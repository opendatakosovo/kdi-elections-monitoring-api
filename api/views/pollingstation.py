from flask import request
from flask.ext.restful import Resource, reqparse
import flask_pymongo

from api import mongo

from api.utils import date_default

import simplejson as json
from .decorators import jsonp

def get_polling_stations_cursor(year=None, election_type=None, commune=None, city=None, name=None, projection=None):
	''' Retrieves polling stations.
	:param year: Year of the election.
	:param election_type: Type of the election, local or general.
	:param commune: The name of the commune.
	:param city: The name of the city.
	:param projection: The projection to apply on the search result.
	'''
	
	# Figure out the name of collection we want to apply the query on.
	# Figure out the name of the collection based on url value.
	collection_name = election_type + 'pollingstations' + str(year)
	
	# Build query base on give URL values.
	query = {}
	
	if commune:
		commune_query = {
			"$or":[
				{'commune.slug.sq': commune},
				{'commune.slug.sr': commune}
			]
		}
	
	if city:
		city_query = {
			"$or":[
				{'city.slug.sq': city},
				{'city.slug.sr': city}
			]
		}
	
	if name:
		name_query = {
			"$or":[
				{'name.slug.sq': name},
				{'name.slug.sr': name}
			]
		}
	
		
	if commune and city and name:
		query = { '$and': [ commune_query, city_query, name_query ] }
		
	elif commune and city:
		query = { '$and': [ commune_query, city_query ] }
		
	elif commune:
		query = commune_query

    #TODO: Build projection   
	#proj = build_projection(projection)
	
	# Run query
	cursor = mongo.db[collection_name].find(query)
	
	return cursor
	
def get_polling_stations(cursor):
	''' Builds a JSON response for a given MongoDB cursor
	
	:param cursor: The MongoDB result set cursor.
	'''
	
	response = json.loads('{}')
	response_to_append_to = response['results'] = []
	
	for idx, bp in enumerate(cursor):
		response_to_append_to.append(bp)
		
	return response

class PollingStation(Resource):
	@jsonp
	def get(self, year=None, election_type=None, commune=None, city=None, name=None):
		''' A get resquest to retrieve a JSON reponse listing the polling stations.
		:param year: Year of the election.
		:param election_type: Type of the election, local or general.
		:param commune: The name of the commune.
		:param city: The name of the city.
		'''
	
		parser = reqparse.RequestParser()
		parser.add_argument('projection')
		
		args = parser.parse_args()
		
		cursor = get_polling_stations_cursor(year, election_type, commune, city, name, args.projection)
		response = get_polling_stations(cursor)
		
		return json.dumps(response, default=date_default)
