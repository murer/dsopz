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

def iterate(dataset, gql, namespace=None, bulkSize=1000, startCursor=None):
    while True:
        yield { 'type': 'cursor', 'cursor': startCursor, 'gql': gql }
        page = query(dataset, gql, namespace, bulkSize, startCursor)
        if not page['entities']:
            return
        startCursor = page.get('endCursor')
        for ent in page['entities']:
            yield { 'type': 'entity', 'entity': ent }


def print_iterate(dataset, gql, namespace=None, msg='', startCursor=None, bulkSize=None):
    it = iterate(dataset, gql, namespace, startCursor=startCursor, bulkSize=bulkSize)
    loaded = 0
    try:
        while True:
            loaded += 1
            if loaded % 1000 == 0:
                print >> sys.stderr, 'loaded', msg, loaded
            entry = it.next();
            if entry['type'] == 'entity':
                print '%s' % (json.dumps(entry['entity'], sort_keys=True))
            else:
                print '### dsopz: %s' % (json.dumps(entry, sort_keys=True))
    except StopIteration:
        pass
    print >> sys.stderr, 'Done', msg, loaded-1

def argparse_prepare(sub):
    sub.add_argument('-d', '--dataset', required=True, help='dataset')
    sub.add_argument('-n', '--namespace', help='namespace')
    sub.add_argument('-q', '--gql', required=True, help='gql')
    sub.add_argument('-c', '--cursor', help='cursor')
    sub.add_argument('-b', '--bulk',  type=int, help='bulk')

def argparse_exec(args):
    print_iterate(args.dataset, args.gql, args.namespace, startCursor=args.cursor, bulkSize=args.bulk)
