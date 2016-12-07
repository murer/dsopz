import oauth
import json
import sys
import argparse

def __parse_entity_results(resp):
    ents = resp['batch'].get('entityResults') or []
    ret = []
    for ent in ents:
        ent = ent['entity']
        copy = {
            'key': {
                'path': ent['key']['path']
            },
            'properties': {}
        }
        for k, v in ent.get('properties', {}).iteritems():
            prop = v.copy()
            excludeFromIndexes = prop.pop('excludeFromIndexes', False)
            prop['excludeFromIndexes'] = excludeFromIndexes
            if v:
                copy['properties'][k] = prop
        ret.append(copy)
    return ret

def query(dataset, gql, namespace=None, limit=1000, startCursor=None):
    url = 'https://datastore.googleapis.com/v1/projects/%s:runQuery' % (dataset)
    queryString = gql
    if limit:
        queryString = '%s limit %i' % (gql, limit)
    if startCursor:
        queryString += ' offset @startCursor'
    params = {
        'partitionId': {
            'projectId': dataset,
            'namespaceId': namespace
        },
        'gqlQuery': {
            'allowLiterals': True,
            'queryString': queryString
        }
    }
    if startCursor:
        params['gqlQuery']['namedBindings'] = { 'startCursor': { 'cursor': startCursor } };
    resp = oauth.oauth_req_json('POST', url, params)
    ret = {}
    ret['entities'] = __parse_entity_results(resp)
    ret['endCursor'] = resp['batch'].get('endCursor')
    return ret

def iterate(dataset, gql, namespace=None, bulkSize=1000):
    startCursor = None
    while True:
        page = query(dataset, gql, namespace, bulkSize, startCursor)
        if not page['entities']:
            return
        startCursor = page.get('endCursor')
        for ent in page['entities']:
            yield ent


def print_iterate(dataset, gql, namespace=None, msg=''):
    it = iterate(dataset, gql, namespace)
    loaded = 0
    try:
        while True:
            loaded += 1
            if loaded % 1000 == 0:
                print >> sys.stderr, 'loaded', msg, loaded
            string = json.dumps(it.next(), sort_keys=True)
            print string
    except StopIteration:
        pass
    print >> sys.stderr, 'Done', msg, loaded-1

def argparse_prepare(sub):
    sub.add_argument('-d', '--dataset', required=True, help='dataset')
    sub.add_argument('-n', '--namespace', help='namespace')
    sub.add_argument('-q', '--gql', required=True, help='gql')

def argparse_exec(args):
    print_iterate(args.dataset, args.gql, args.namespace)
