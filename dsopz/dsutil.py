from dsopz.config import config
from dsopz import io
from dsopz import util

def resolve_query(dataset, namespace, gql=None, query=None, plain=None, gz=None):
    if gql or query:
        ret = gql or query
        return { 'dataset': dataset, 'namespace': namespace, 'queries': ret }
    if plain or gz:
        with io.jreader(plain, gz) as f:
            header = next(f)
            queries = header['queries']
            for line in f:
                queryidx = line['queryIndex']
                cursor = line['cursor']
                queries[queryidx]['startCursor'] = cursor
            return header
    raise Error('error')

def resolve_mutation_skip(resume):
    if not resume:
        return 0
    try:
        with io.jreader(resume) as r:
            ret = None
            for l in r:
                ret = l
            return ret['processed']
    except FileNotFoundError:
        return 0
