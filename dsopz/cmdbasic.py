from dsopz.config import config
from dsopz import io
from dsopz import dsutil
from dsopz.datastore import stream_block, mutation
from dsopz.processor import blockify
from dsopz import util
from os import devnull
import logging as log
import json as JSON

class Error(Exception):
    """Exceptions"""

def cmd_download():
    if (config.args.gql or config.args.query) and not config.args.dataset:
            raise Error('dataset is required for query or gql')
    if (config.args.resume or config.args.resume_gz) and (config.args.dataset or config.args.namespace):
        raise Error('dataset/namespace is not allowed for resume or resume_gz')
    header = dsutil.resolve_query(config.args.dataset, config.args.namespace, config.args.gql, config.args.query, config.args.resume, config.args.resume_gz)
    count = 0
    with io.jwriter(config.args.file, config.args.file_gz, append=config.args.append) as f:
        result = stream_block(header['dataset'], header['namespace'], header['query'])
        query = next(result)
        log.info('query: %s', JSON.dumps(query))
        if not config.args.append:
            f.write({'dataset': header['dataset'], 'namespace': header['namespace'], 'query': query})
        for block in result:
            count = count + len(block['batch']['entityResults'])
            for entity in block['batch']['entityResults']:
                f.write(entity)
            log.info('Downloaded: %s', count)

def cmd_kind():
    header = dsutil.resolve_query(config.args.dataset, config.args.namespace, 'select * from __kind__', None, None, None)
    with io.jwriter(config.args.file, config.args.file_gz, append=False) as f:
        result = stream_entity(header['dataset'], header['namespace'], header['query'])
        query = next(result)
        log.info('query: %s', JSON.dumps(query))
        f.write({'dataset': header['dataset'], 'namespace': header['namespace'], 'query': query})
        for line in result:
            f.write(line)

def cmd_namespace():
    header = dsutil.resolve_query(config.args.dataset, None, 'select * from __namespace__', None, None, None)
    with io.jwriter(config.args.file, config.args.file_gz, append=False) as f:
        result = stream_entity(header['dataset'], header['namespace'], header['query'])
        query = next(result)
        log.info('query: %s', JSON.dumps(query))
        f.write({'dataset': header['dataset'], 'namespace': header['namespace'], 'query': query})
        for line in result:
            f.write(line)

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
                    r.write(count)
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
                r.write(count)
    finally:
        util.close(r)



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
