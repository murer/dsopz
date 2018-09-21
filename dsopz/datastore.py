from dsopz.http import req_json
from dsopz.oauth import oauth
from dsopz.config import config
import json as JSON

class Error(Exception):
	"""Exceptions"""

def ckey(k, dataset='dsopzproj', namespace=None):
    if len(k) % 2 != 0:
        raise Error('must be even %s' % (k))
    ret = {
        'partitionId': { 'projectId': dataset },
        'path': []
    }
    for i in range(0, len(k), 2):
        ret['path'].append({ 'kind': k[i], 'name': k[i+1] })
    if namespace:
        ret['partitionId']['namespaceId'] = namespace
    return ret

def cprop(name, type, value):
    return {
        name: {
            '%sValue' % (type): value
        }
    }

def centity(k, *props):
    entity = { 'key': k, 'properties': {}}
    for i in props:
        entity['properties'].update(i)
    return entity

def run_query(
        dataset,
        namespace,
        query):
    url = '%s/v1/projects/%s:runQuery' % (config.args.url, dataset)
    body = {
        'partitionId': {
            'projectId': dataset,
            'namespaceId': namespace
        }
    }
    if isinstance(query, dict):
        body['query'] = query
    else:
        body['gqlQuery'] = {
            'allowLiterals': True,
            'queryString': query
        }
    resp = req_json('POST', url, body, {
        'Authorization': 'Bearer %s' % (oauth.access_token())
    })
    ret = resp['body']
    ret['batch']['entityResults'] = ret['batch'].get('entityResults', [])
    ret['query'] = ret.get('query', query)
    return ret

def lookup(dataset, keys):
    url = '%s/v1/projects/%s:lookup' % (config.args.url, dataset)
    body = { 'keys': keys }
    resp = req_json('POST', url, body, {
        'Authorization': 'Bearer %s' % (oauth.access_token())
    })
    ret = resp['body']
    return ret

def commit(dataset, mutations):
    url = '%s/v1/projects/%s:commit' % (config.args.url, dataset)
    resp = req_json('POST', url, mutations, {
        'Authorization': 'Bearer %s' % (oauth.access_token())
    })
    ret = resp['body']
    return ret

def mutation(dataset, upserts=None, removes=None):
    body = { 'mode': 'NON_TRANSACTIONAL', 'mutations': [] }
    if upserts:
        body['mutations'].extend([ { 'upsert': entity } for entity in upserts ])
    if removes:
        body['mutations'].extend([ { 'delete': entity } for entity in removes ])
    return commit(dataset, body)

def abc(dataset, namespace, query):
    yield run_query(dataset, namespace, query)
