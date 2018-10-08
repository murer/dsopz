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

    def __init__(self, dataset, namespace, kind, range_file, range_file_gz, scatter, file, file_gz):
        self._dataset = dataset
        self._namespace = namespace
        self._kind = kind
        self._range_file = range_file
        self._range_file_gz = range_file_gz
        self._scatter = scatter
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

    def _query_scatters(self):
        return [i for i in dsutil.download(
            dataset=self._dataset, namespace=self._namespace,
            gql=None, query=[{"kind": [{"name": self._kind}], "order": [{"property": {"name": "__scatter__"}, "direction": "ASCENDING"}]}], kind=None,
            resume=None, resume_gz=None,
            limit=self._scatter
        )]

    def _read_scatters(self):
        ret = []
        with io.jreader(self._range_file, self._range_file_gz) as f:
            for line in f:
                ret.append(line)
        return ret

    def _read_keys(self):
        entities = self._query_scatters() if self._scatter else self._read_scatters()
        ret = []
        for entity in entities:
            if entity.get('entity'):
                k = entity['entity']['key']
                set_partition(k, self._dataset, self._namespace)
                ret.append(k)
        ret = sorted(ret, key=lambda i: [[p['kind'], p.get('name', p.get('id'))] for p in i['path']])
        self._keys = ret

    def execute(self):
        self._read_keys()
        self._produce_ranges()
        self._prepare_range_queries()
        dsutil.download_to_file(
            dataset=self._dataset,
            namespace=self._namespace,
            file=self._file,
            file_gz=self._file_gz,
            gql=None,
            query=self._queries,
            kind=None,
            resume=None,
            resume_gz=None,
            append=False
        )
        log.info('Done')

def cmd_scatter():
    Scatter(
        config.args.dataset,
        config.args.namespace,
        config.args.kind,
        config.args.range_file,
        config.args.range_file_gz,
        config.args.scatter,
        config.args.file,
        config.args.file_gz
    ).execute()

subparser = config.add_parser('scatter', cmd_scatter)
subparser.add_argument('-d', '--dataset', required=True, help='dataset')
subparser.add_argument('-n', '--namespace', required=True, help='Namespace')
subparser.add_argument('-k', '--kind', required=True, help='kind')
group = subparser.add_mutually_exclusive_group(required=True)
group.add_argument('-r', '--range-file', help='input file key ranges or - for stdin')
group.add_argument('-rgz', '--range-file-gz', help='input gzip file key ranges')
group.add_argument('-s', '--scatter', type=int, help='number of scatter to use')
group = subparser.add_mutually_exclusive_group(required=True)
group.add_argument('-f', '--file', help='output directory')
group.add_argument('-fgz', '--file-gz', help='output gzip directory')
