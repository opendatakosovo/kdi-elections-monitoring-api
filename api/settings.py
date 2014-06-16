import logging
import logging.handlers
import os
import socket
_basedir = os.path.abspath(os.path.dirname(__file__))

SERVER_PORT=5000

MONGO_URI='mongodb://localhost:27017/generalelections2014'

LOG_LEVEL='WARNING'
LOG_PATH='logs/kdi-elections-monitoring-api.log'
