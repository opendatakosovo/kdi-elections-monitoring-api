import logging

def date_default(obj):
	''' Used to properly encode dates when calling json.dumps.
	override date format on bson dump, not sure if there's a better way.
	e.g. json.dumps(myjson, default=date_default).
	'''
	if isinstance(obj, datetime.datetime):
		if obj.utcoffset() is not None:
			obj = obj - obj.utcoffset()
		return obj.strftime('%Y-%m-%dT%H:%M:%SZ')
	else:
		return json_util.default(obj)
		
class FullModuleNameFormatter(logging.Formatter):
	'''supports additional LogRecord attribute:
	%(modulepath)s is path to module file relative to current working directory.
	Does not include trailing .py or /__init__.py
	'''
	def format(self, record):
		record.__dict__['modulepath'] = get_module_path(record.pathname)
		return super(FullModuleNameFormatter, self).format(record)
