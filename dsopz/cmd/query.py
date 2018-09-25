import sys
from dsopz.config import config
from dsopz.datastore import stream_entity
import json as JSON

def cmd_query():
    result = stream_entity(config.args.dataset, config.args.namespace, config.args.gql)
    query = next(result)
    print(JSON.dumps({'query': query, 'dataset': dataset, 'namespace': namespace}))
    for entity in result:
        print(JSON.dumps(entity))

def cmd_resume():
    head = next(sys.stdin)
    head = JSON.loads(head)
    print('head', head)
    for line in sys.stdin:
        line = line.strip()
        entity = JSON.loads(line)
        print(line)
        head['query']['startCursor'] = entity['cursor']
    result = stream_entity(head['dataset'], head['namespace'], head['query'])
    next(result)
    for entity in result:
        print(JSON.dumps(entity))



subparser = config.add_parser('query', cmd_query)
subparser.add_argument('-d', '--dataset', required=True, help='dataset')
subparser.add_argument('-n', '--namespace', help='namespace')
subparser.add_argument('-g', '--gql', required=True, help='gql')

subparser = config.add_parser('resume', cmd_resume)
