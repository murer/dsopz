from dsopz.http import req_json
from dsopz.oauth import oauth
from dsopz.config import config
import json as JSON

class Error(Exception):
    """Exceptions"""

def _set_partition(k, dataset, namespace):
    if not dataset:
        k.pop('partitionId')
        return k
    k['partitionId'] = { 'projectId': dataset }
    if namespace:
        k['partitionId']['namespaceId'] = namespace
    return k

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
    for entity in ret['batch']['entityResults']:
        _set_partition(entity['entity']['key'], None, None)
    return ret

def lookup(dataset, namespace, keys):
    url = '%s/v1/projects/%s:lookup' % (config.args.url, dataset)
    keys = [ _set_partition({ 'path': k['path'] }, dataset, namespace) for k in keys ]
    body = { 'keys': keys }
    resp = req_json('POST', url, body, {
        'Authorization': 'Bearer %s' % (oauth.access_token())
    })
    ret = resp['body']
    if ret.get('deferred'):
        raise Error('idk what is deferred')
    ret = ret.get('found', [])
    for entity in ret:
        _set_partition(entity['entity']['key'], None, None)
    return ret

import threading

CC = 1
lock = threading.Lock()

def C():
    global CC
    global lock
    with lock:
        CC = CC + 1
        return CC

def commit(dataset, namespace, mutations):
    for m in mutations['mutations']:
        if m.get('insert'):
            _set_partition(m['insert']['key'], dataset, namespace)
        if m.get('update'):
            _set_partition(m['update']['key'], dataset, namespace)
        if m.get('upsert'):
            _set_partition(m['upsert']['key'], dataset, namespace)
        if m.get('delete'):
            _set_partition(m['delete'], dataset, namespace)
    with open('/home/murer/tmp/d/c-%s' % (C()), 'w') as f:
        f.write(JSON.dumps(mutations))
        f.write('\n')
        url = '%s/v1/projects/%s:commit' % (config.args.url, dataset)
        resp = req_json('POST', url, mutations, {
            'Authorization': 'Bearer %s' % (oauth.access_token())
        })
        ret = resp['body']
        f.write(JSON.dumps(ret))
        return ret

def mutation(dataset, namespace, upserts=None, removes=None):
    body = { 'mode': 'NON_TRANSACTIONAL', 'mutations': [] }
    if upserts:
        for entity in upserts:
            body['mutations'].append({ 'upsert': entity })
    if removes:
        for k in removes:
            body['mutations'].append({ 'delete': k })
    return commit(dataset, namespace, body)

def stream_block(dataset, namespace, query):
    first = True
    while True:
        result = run_query(dataset, namespace, query)
        query = result['query']
        if first:
            yield query
            first = False
        if not result['batch']['entityResults']:
            return
        yield result
        query['startCursor'] = result['batch']['endCursor']

def stream_entity(dataset, namespace, query):
    result = stream_block(dataset, namespace, query)
    yield next(result)
    for k in result:
        for entity in k['batch']['entityResults']:
            yield entity
