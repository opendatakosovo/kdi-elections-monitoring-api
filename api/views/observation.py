from flask import request
from flask.ext.restful import Resource, reqparse
import flask_pymongo

from api import mongo

from api.utils import date_default

import simplejson as json

def get_observations_cursor(year=None, election_type=None, election_round=None, json_query=None):
	'''Retrieves observations as a cursor response.
	:param year: the year of the observed elections.
	:param election_type: the type of election observed, local or general.
	:param election_round: The round of the election, first or second.
	:param json_query: the JSON query string to apply.
	'''
	
	# Create JSON object representation of the JSON query string.
	json_query_obj = json.loads(json_query)
	
	# Figure out the name of collection we want to apply the query on.
	# Figure out the name of the collection based on url value.
	collection_name = election_type + election_round + str(year)
	
	# Run query
	cursor = mongo.db[collection_name].find(json_query_obj)
	
	# Return result as cursor
	return cursor

def get_observations(cursor):
	''' Return a JSON result response based on the given cursor.
	:param cursor: The MongoDB result set cursor.
	'''
	
	# Build JSON response from cursor
	response = json.loads('{}')
	response_to_append_to = response['results'] = []
	
	for idx, bp in enumerate(cursor):
		response_to_append_to.append(bp)
		
	return response
	
class Observation(Resource):
	def post(self, year, election_type, election_round):
		''' POST request to search observation documents.
		:param year: the year of the observed elections.
		:param election_type: the type of election observed, local or general.
		:param election_round: The round of the election, first or second.
		'''
		
		# Get the JSON query string
		json_query = json.loads(request.data)
		
		# Apply query, get response.
		cursor = get_observations_cursor(year, election_type, election_round, json_query)
		response = get_observations(cursor)
		
		# Return response
		return json.dumps(response, default=date_default)
