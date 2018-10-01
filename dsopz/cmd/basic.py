from dsopz.config import config
from dsopz import io
from dsopz import dsutil
from dsopz.datastore import stream_entity

class Error(Exception):
    """Exceptions"""

def cmd_download():
    if (config.args.gql or config.args.query) and not config.args.dataset:
            raise Error('dataset is required for query or gql')
    if (config.args.resume or config.args.resume_gz) and (config.args.dataset or config.args.namespace):
        raise Error('dataset/namespace is not allowed for resume or resume_gz')
    header = dsutil.resolve_query(config.args.dataset, config.args.namespace, config.args.gql, config.args.query, config.args.resume, config.args.resume_gz)
    with io.jwriter(config.args.file, config.args.file_gz, append=config.args.append) as f:
        result = stream_entity(header['dataset'], header['namespace'], header['query'])
        query = next(result)
        if not config.args.append:
            f.write({'dataset': header['dataset'], 'namespace': header['namespace'], 'query': query})
        for line in result:
            f.write(line)

def cmd_kind():
    return True

def cmd_namespace():
    return True

def cmd_upsert():
    import json as JSON
    with io.jreader(config.args.file, config.args.file_gz) as f:
        for line in f:
            entity = line.get('entity')
            if entity:
                print(JSON.dumps(entity))
    return True

def cmd_rm():
    return True


subparser = config.add_parser('download', cmd_download)
subparser.add_argument('-d', '--dataset', help='dataset. Required for gql or query')
subparser.add_argument('-n', '--namespace', help='Namespace. Ignored for resume or resume-gz')
group = subparser.add_mutually_exclusive_group(required=True)
group.add_argument('-g', '--gql', help='gql')
group.add_argument('-q', '--query', help='json query')
group.add_argument('-r', '--resume', help='json query and cursor from file')
group.add_argument('-rgz', '--resume-gz', help='json query and cursor from gzip file or - for stdin')
group = subparser.add_mutually_exclusive_group(required=True)
group.add_argument('-f', '--file', help='output file or - for stdout')
group.add_argument('-fgz', '--file-gz', help='output gzip file or - for stdout')
subparser.add_argument('-a', '--append', action='store_true', help='append into file and do not write header')

subparser = config.add_parser('kind', cmd_kind)
subparser.add_argument('-d', '--dataset', required=True, help='dataset')
subparser.add_argument('-n', '--namespace', help='namespace')
subparser.add_argument('-a', '--all', action='store_true', help='print "__.*__" also')
group = subparser.add_mutually_exclusive_group(required=True)
group.add_argument('-f', '--file', help='output file or - for stdout')
group.add_argument('-fgz', '--file-gz', help='output gzip file or - for stdout')

subparser = config.add_parser('namespace', cmd_namespace)
subparser.add_argument('-d', '--dataset', required=True, help='dataset')
group = subparser.add_mutually_exclusive_group(required=True)
group.add_argument('-f', '--file', help='output file or - for stdout')
group.add_argument('-fgz', '--file-gz', help='output gzip file or - for stdout')

subparser = config.add_parser('upsert', cmd_upsert)
subparser.add_argument('-d', '--dataset', required=True, help='dataset')
subparser.add_argument('-n', '--namespace', help='namespace')
subparser.add_argument('-p', '--progress', help='file necessary to track and resume the process. Entities may be upsert twice anyway')
group = subparser.add_mutually_exclusive_group(required=True)
group.add_argument('-f', '--file', help='input file or - for stdin')
group.add_argument('-fgz', '--file-gz', help='input gzip file or - for stdin')

subparser = config.add_parser('rm', cmd_namespace)
subparser.add_argument('-d', '--dataset', required=True, help='dataset')
subparser.add_argument('-n', '--namespace', help='namespace')
group = subparser.add_mutually_exclusive_group(required=True)
group.add_argument('-f', '--file', help='input file or - for stdin')
group.add_argument('-fgz', '--file-gz', help='input gzip file or - for stdin')
