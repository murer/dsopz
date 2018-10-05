from dsopz.config import config
from dsopz import io
from dsopz import dsutil
from dsopz.datastore import stream_block, mutation, stream_entity
from dsopz.processor import blockify, merge_gens, AsyncGen, dispatch
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
        with AsyncGen(merge_gens(results)) as r:
            for queryidx, result in r:
                count[queryidx] = count[queryidx] + len(result['batch']['entityResults'])
                for entity in result['batch']['entityResults']:
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
        gql=[ 'select * from __kind__' ] if config.args.all else [
                "select * from __kind__ where __key__ < KEY(__kind__, '__')",
                "select * from __kind__ where __key__ > KEY(__kind__, '__\ufffd')" ]
    )

def cmd_namespace():
    _download(
        dataset=config.args.dataset,
        file=config.args.file,
        file_gz=config.args.file_gz,
        kind=[ '__namespace__' ]
    )

def _resume(file, file_gz, resume, skip, parser):
    start = None
    block = []
    with io.jreader(file, file_gz) as f:
        f = enumerate(f)
        for i in range(skip):
            log.info('Skipping: %s', i)
            next(f)
        for idx, line in f:
            if start == None:
                start = idx
            line = parser(line)
            if line:
                block.append(line)
            if len(block) >= 500:
                yield (start, idx, block)
                block = []
                start = None
        if len(block) > 0:
            yield (start, idx, block)


def cmd_upsert():
    skip = dsutil.resolve_mutation_skip(config.args.resume)
    log.info('Skip: %s', skip)
    buffer = []
    for start, end, block in _resume(config.args.file, config.args.file_gz, config.args.resume, skip, lambda x: x.get('entity')):
        log.info('Processing: [%s - %s], len: %s', start, end, len(block))
        while len(buffer) >= 20:
            p_start, p_end, p_block, p_fut = buffer.pop(0)
            log.info('Waiting for: [%s - %s], len: %s', p_start, p_end, len(p_block))
            p_fut.result()
            io.write_all(config.args.resume, append=True, lines=[{'processed':p_end+1}])
        fut = dispatch(mutation, config.args.dataset, config.args.namespace, upserts=block)
        buffer.append( (start, end, block, fut) )
    while len(buffer) > 0:
        p_start, p_end, p_block, p_fut = buffer.pop(0)
        log.info('Last waiting for: [%s - %s], len: %s', p_start, p_end, len(p_block))
        p_fut.result()
        io.write_all(config.args.resume, append=True, lines=[{'processed':p_end+1}])

def _mutation(dataset, namespace, file, file_gz, resume, op, parser):
    skip = dsutil.resolve_mutation_skip(resume)
    log.info('Already processed: %s', skip)
    count = 0
    r = io.jwriter(resume, append=True) if resume else None
    try:
        with io.jreader(file, file_gz) as f:
            for block in blockify(f, 500, parser, skip):
                count = count + len(block)
                log.info('Processing: %s', count)
                if op == 'upsert':
                    mutation(dataset, namespace, upserts=block)
                elif op == 'remove':
                    mutation(dataset, namespace, removes=block)
                else:
                    raise Error('unknown: %s' % (op))
                if r:
                    r.write({'processed': count})
    finally:
        util.close(r)

def cmd_upsertx():
    _mutation(
        config.args.dataset,
        config.args.namespace,
        config.args.file,
        config.args.file_gz,
        config.args.resume,
        'upsert',
        lambda x: x.get('entity')
    )

def cmd_rm():
    _mutation(
        config.args.dataset,
        config.args.namespace,
        config.args.file,
        config.args.file_gz,
        config.args.resume,
        'remove',
        lambda x: x.get('entity', {}).get('key')
    )

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
subparser.add_argument('-a', '--all', action='store_true', help='include reserved (__*__) kinds')
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
