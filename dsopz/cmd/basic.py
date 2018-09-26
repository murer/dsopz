import sys
from dsopz.config import config
from dsopz.datastore import stream_entity, mutation
import json as JSON

def cmd_query():
    result = stream_entity(config.args.dataset, config.args.namespace, config.args.gql)
    query = next(result)
    print(JSON.dumps({'query': query, 'dataset': config.args.dataset, 'namespace': config.args.namespace}))
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
    result = stream_entity(head['dataset'], head.get('namespace'), head['query'])
    next(result)
    for entity in result:
        print(JSON.dumps(entity))

def cmd_kind():
    result = stream_entity(config.args.dataset, config.args.namespace, 'select __key__ from __kind__')
    query = next(result)
    print(JSON.dumps({'query': query, 'dataset': config.args.dataset, 'namespace': config.args.namespace}))
    for entity in result:
        k = entity['entity']['key']
        name = k['path'][0]['name']
        if name.startswith('__') and not config.args.all:
            continue
        print(JSON.dumps(entity))

def cmd_namespace():
    result = stream_entity(config.args.dataset, None, 'select __key__ from __namespace__')
    query = next(result)
    print(JSON.dumps({'query': query, 'dataset': config.args.dataset }))
    for entity in result:
        print(JSON.dumps(entity))

def cmd_upsert():
    block = []
    for line in sys.stdin:
        line = line.strip()
        entity = JSON.loads(line)
        if entity.get('entity'):
            entity['entity']['key']['partitionId']['projectId'] = config.args.dataset
            entity['entity']['key']['partitionId']['namespaceId'] = config.args.namespace
            block.append(entity['entity'])
        if len(block) > 2:
            mutation(config.args.dataset, upserts=block)
            block = []
    if len(block) > 0:
        mutation(config.args.dataset, upserts=block)

def cmd_remove():
    block = []
    for line in sys.stdin:
        line = line.strip()
        entity = JSON.loads(line)
        if entity.get('entity'):
            block.append({
                'partitionId': {
                    'projectId': config.args.dataset,
                    'namespaceId': config.args.namespace
                },
                'path': entity['entity']['key']['path']
            })
        if len(block) > 1000:
            mutation(config.args.dataset, removes=block)
            block = []
    if len(block) > 0:
        mutation(config.args.dataset, removes=block)


subparser = config.add_parser('query', cmd_query)
subparser.add_argument('-d', '--dataset', required=True, help='dataset')
subparser.add_argument('-n', '--namespace', help='namespace')
subparser.add_argument('-g', '--gql', required=True, help='gql')

subparser = config.add_parser('resume', cmd_resume)

subparser = config.add_parser('kind', cmd_kind)
subparser.add_argument('-d', '--dataset', required=True, help='dataset')
subparser.add_argument('-n', '--namespace', help='namespace')
subparser.add_argument('-a', '--all', action='store_true', help='print "__.*__" also')

subparser = config.add_parser('namespace', cmd_namespace)
subparser.add_argument('-d', '--dataset', required=True, help='dataset')

subparser = config.add_parser('upsert', cmd_upsert)
subparser.add_argument('-d', '--dataset', required=True, help='dataset')
subparser.add_argument('-n', '--namespace', help='namespace')

subparser = config.add_parser('remove', cmd_remove)
subparser.add_argument('-d', '--dataset', required=True, help='dataset')
subparser.add_argument('-n', '--namespace', help='namespace')
