from dsopz.config import config
from dsopz import io
from dsopz import dsutil
from dsopz.datastore import stream_block, mutation, stream_entity, set_partition
from dsopz.processor import blockify, merge_gens, AsyncGen, dispatch
from dsopz import util
import logging as log
import os
import json as JSON

class Error(Exception):
    """Exceptions"""

class Scatter(object):

    def __init__(self, dataset, namespace, kind, range_file, range_file_gz, file, file_gz):
        self._dataset = dataset
        self._namespace = namespace
        self._kind = kind
        self._range_file = range_file
        self._range_file_gz = range_file_gz
        self._file = file
        self._file_gz = file_gz

    def _parse_col(self, line):
        if not line:
            return None
        return line['entity']['key']

    def _produce_ranges(self):
        self._ranges = []
        prev = None
        for range in self._keys:
            self._ranges.append((prev, range))
            prev = range
        self._ranges.append((prev, None))

    def _prepare_range_query(self, s, e):
        filters = []
        ret = { "kind" : [{"name": self._kind}], "filter" : { "compositeFilter" : { "op" : "AND", "filters" : filters } } }
        if s:
            filters.append({
                "propertyFilter" : {
                    "value" : {
                        "keyValue" : s
                    },
                    "property" : { "name" : "__key__" },
                    "op" : "GREATER_THAN_OR_EQUAL"
                }
            })
        if e:
            filters.append({
                "propertyFilter" : {
                    "op" : "LESS_THAN",
                    "property" : { "name" : "__key__"  },
                    "value" : {
                        "keyValue" : e
                    }
                }
            })
        return ret

    def _prepare_range_queries(self):
        self._queries = []
        for s, e in self._ranges:
            self._queries.append(self._prepare_range_query(s, e))

    def _read_keys(self):
        ret = []
        with io.jreader(self._range_file, self._range_file_gz) as f:
            for line in f:
                if line.get('entity'):
                    k = line['entity']['key']
                    set_partition(k, self._dataset, self._namespace)
                    ret.append(k)
        ret = sorted(ret, key=lambda i: [[p['kind'], p.get('name', p.get('id'))] for p in i['path']])
        self._keys = ret

    def execute(self):
        self._read_keys()
        self._produce_ranges()
        self._prepare_range_queries()
        resume = os.path.isfile(self._file or self._file_gz)
        dsutil.download_to_file(
            dataset=None if resume else self._dataset,
            namespace=None if resume else self._namespace,
            file=self._file,
            file_gz=self._file_gz,
            gql=None,
            query=None if resume else self._queries,
            kind=None,
            resume=self._file if resume else None,
            resume_gz=self._file_gz if resume else None,
            append=resume
        )

        """
        with io.jreader(self._range_file, self._range_file_gz) as f:
            self._header = next(f)
            print('xxx', self._header)
            self._kind = self._header['queries'][0]['kind']
            output_dir = self._output or self._output_gz
            util.makedirs(output_dir)
            queries = []
            futs = []
            for idx, ses in enumerate(blockify(self._produce_ranges(f), config.args.queries_per_file)):
                queries = [self._prepare_range_query(s, e) for s, e in ses]
                print('q', len(queries))
                output_file = os.path.join(output_dir, 'part-%s' % (idx))
                print(output_file, self._kind[0]['name'], self._header['dataset'], self._header['namespace'])
                dataset=self._header['dataset']
                namespace=self._header['namespace']
                resume = None
                append = False
                output_file_gz = None
                resume_gz = None
                if self._output_gz:
                    output_file_gz = output_file
                    output_file = None
                if os.path.isfile(output_file or output_file_gz):
                    resume = output_file
                    resume_gz = output_file_gz
                    dataset = None
                    namespace = None
                    queries = None
                    append = True
                while len(futs) >= 3:
                    futs.pop(0).result()
                futs.append(dispatch(dsutil.download_to_file,
                    dataset=dataset,
                    namespace=namespace,
                    file=output_file,
                    file_gz=output_file_gz,
                    gql=None,
                    query=queries,
                    kind=None,
                    resume=resume,
                    resume_gz=resume_gz,
                    append=append
                ))
            while len(futs) > 0:
                futs.pop(0).result()
        """


def cmd_scatter():
    Scatter(
        config.args.dataset,
        config.args.namespace,
        config.args.kind,
        config.args.range_file,
        config.args.range_file_gz,
        config.args.file,
        config.args.file_gz
    ).execute()

subparser = config.add_parser('scatter', cmd_scatter)
subparser.add_argument('-d', '--dataset', required=True, help='dataset')
subparser.add_argument('-n', '--namespace', required=True, help='Namespace')
subparser.add_argument('-k', '--kind', required=True, help='kind')
group = subparser.add_mutually_exclusive_group(required=True)
group.add_argument('-r', '--range-file', help='input file or - for stdin')
group.add_argument('-rgz', '--range-file-gz', help='input gzip file')
group = subparser.add_mutually_exclusive_group(required=True)
group.add_argument('-f', '--file', help='output directory')
group.add_argument('-fgz', '--file-gz', help='output gzip directory')
