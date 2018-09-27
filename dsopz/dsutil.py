from dsopz.config import config
from dsopz import io

def resolve_query(dataset, namespace, gql=True, query=None, plain=None, gz=None):
    if gql or query:
        ret = gql or query
        return { 'dataset': dataset, 'namespace': namespace, 'query': ret }
    if plain or gz:
        with io.jreader(plain, gz) as f:
            header = next(f)
            query = header['query']
            lastLine = None
            for line in f:
                lastLine = line
            query['startCursor'] = lastLine['cursor'] if lastLine else query['startCursor']
            return header
    raise Error('error')
