from dsopz.config import config
from dsopz import io

def resolve_query(gql=True, query=None, plain=None, gz=None):
    if gql or query:
        return gql or query
    if plain or gz:
        with io.jreader(plain, gz) as f:
            header = next(f)
            query = header['query']
            lastLine = None
            for line in f:
                lastLine = f
            query['startCursor'] = line['cursor']
            return query
    raise Error('error')
