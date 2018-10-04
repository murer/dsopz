from dsopz.config import config
from dsopz import io
from dsopz import dsutil
from dsopz.datastore import stream_block, mutation, stream_entity
from dsopz.processor import blockify
from dsopz import util
from os import devnull
import logging as log
import json as JSON

class Error(Exception):
    """Exceptions"""

def _download(dataset=None, namespace=None, file=None, file_gz=None, gql=None, query=None, kind=None, resume=None, resume_gz=None, append=None):
    if (gql or query or kind) and not dataset:
            raise Error('dataset is required for query, gql or kind')
    if (resume or resume_gz) and (dataset or namespace):
        raise Error('dataset/namespace is not allowed for resume or resume_gz')
    header = dsutil.resolve_query(dataset, namespace, gql, query, kind, resume, resume_gz)
    count = [0] * len(header['queries'])
    with io.jwriter(file, file_gz, append=append) as f:
        results = [stream_block(header['dataset'], header['namespace'], q) for q in header['queries']]
        queries = [next(h) for h in results]
        log.info('queries: %s', JSON.dumps(queries))
        if not append:
            f.write({'dataset': header['dataset'], 'namespace': header['namespace'], 'queries': queries})
        for queryidx, result in enumerate(results):
            for block in result:
                count[queryidx] = count[queryidx] + len(block['batch']['entityResults'])
                for entity in block['batch']['entityResults']:
                    entity['queryIndex'] = queryidx
                    f.write(entity)
                log.info('Downloaded: %s', count)

def cmd_download():
    _download(
        dataset=config.args.dataset,
        namespace=config.args.namespace,
        file=config.args.file,
        file_gz=config.args.file_gz,
        gql=config.args.gql,
        query=config.args.query,
        kind=config.args.kind,
        resume=config.args.resume,
        resume_gz=config.args.resume_gz,
        append=config.args.append
    )

def cmd_kind():
    _download(
        dataset=config.args.dataset,
        namespace=config.args.namespace,
        file=config.args.file,
        file_gz=config.args.file_gz,
        kind=[ '__kind__' ]
    )

def cmd_namespace():
    _download(
        dataset=config.args.dataset,
        file=config.args.file,
        file_gz=config.args.file_gz,
        kind=[ '__namespace__' ]
    )

def cmd_upsert():
    skip = dsutil.resolve_mutation_skip(config.args.resume)
    log.info('Already processed: %s', skip)
    count = 0
    r = io.jwriter(config.args.resume, append=True) if config.args.resume else None
    try:
        with io.jreader(config.args.file, config.args.file_gz) as f:
            for block in blockify(f, 1000, lambda x: x.get('entity'), skip):
                count = count + len(block)
                log.info('Processing: %s', count)
                mutation(config.args.dataset, config.args.namespace, upserts=block)
                if r:
                    r.write({'processed': count})
    finally:
        util.close(r)

def cmd_rm():
    skip = dsutil.resolve_mutation_skip(config.args.resume)
    log.info('Already processed: %s', skip)
    count = 0
    r = io.jwriter(config.args.resume, append=True) if config.args.resume else None
    try:
        with io.jreader(config.args.file, config.args.file_gz) as f:
            for block in blockify(f, 1000, lambda x: x.get('entity', {}).get('key'), skip):
                count = count + len(block)
                log.info('Processing: %s', count)
                mutation(config.args.dataset, config.args.namespace, removes=block)
                r.write({'processed': count})
    finally:
        util.close(r)

subparser = config.add_parser('download', cmd_download)
subparser.add_argument('-d', '--dataset', help='dataset. Required for gql or query')
subparser.add_argument('-n', '--namespace', help='Namespace. Ignored for resume or resume-gz')
group = subparser.add_mutually_exclusive_group(required=True)
group.add_argument('-g', '--gql', nargs='+', help='gql')
group.add_argument('-q', '--query', nargs='+', help='json query')
group.add_argument('-k', '--kind', nargs='+', help='kinds')
group.add_argument('-r', '--resume', help='json query and cursor from file')
group.add_argument('-rgz', '--resume-gz', help='json query and cursor from gzip file or - for stdin')
group = subparser.add_mutually_exclusive_group(required=True)
group.add_argument('-f', '--file', help='output file or - for stdout')
group.add_argument('-fgz', '--file-gz', help='output gzip file or - for stdout')
subparser.add_argument('-a', '--append', action='store_true', help='append into file and do not write header')

subparser = config.add_parser('kind', cmd_kind)
subparser.add_argument('-d', '--dataset', required=True, help='dataset')
subparser.add_argument('-n', '--namespace', help='namespace')
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
subparser.add_argument('-r', '--resume', help='file necessary to track and resume the process. Entities may be upsert twice anyway')
group = subparser.add_mutually_exclusive_group(required=True)
group.add_argument('-f', '--file', help='input file or - for stdin')
group.add_argument('-fgz', '--file-gz', help='input gzip file or - for stdin')

subparser = config.add_parser('rm', cmd_rm)
subparser.add_argument('-d', '--dataset', required=True, help='dataset')
subparser.add_argument('-n', '--namespace', help='namespace')
subparser.add_argument('-r', '--resume', help='file necessary to track and resume the process. Entities may be upsert twice anyway')
group = subparser.add_mutually_exclusive_group(required=True)
group.add_argument('-f', '--file', help='input file or - for stdin')
group.add_argument('-fgz', '--file-gz', help='input gzip file or - for stdin')
