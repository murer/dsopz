import json

def get_kind(obj):
	path = obj['key']['path']
	i = len(path)
	last = path[i - 1]
	return last['kind']

def prop(entity, name):
	if name == '__key__':
		return entity['key']['path']
	return entity['properties'].get(name)

def prop_value(entity, name):
	p = prop(entity, name)
	if not p or name == '__key__':
		return p, None
	for k, v in p.iteritems():
		if k.endswith('Value'):
			return v, k
	return None, None

def human_key(key):
	if not key:
		return 'null'
	if type(key) == type(dict()):
		key = key.get('path')
	if not key:
		return 'null'
	ret = ''
	for k in key:
		ret += ('%s/%s' % (k['kind'], json.dumps(k.get('name') or k.get('id'))))
	return ret

