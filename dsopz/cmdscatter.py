from dsopz.config import config
from dsopz import io
from dsopz import dsutil
from dsopz.datastore import stream_block, mutation, stream_entity
from dsopz.processor import blockify, merge_gens, AsyncGen, dispatch
from dsopz import util
import logging as log
import os
import json as JSON

class Error(Exception):
    """Exceptions"""

class Scatter(object):

    def __init__(self, range_file, range_file_gz, output):
        self._range_file = range_file
        self._range_file_gz = range_file_gz
        self._output = output

    def _parse_col(self, line):
        if not line:
            return None
        return line['entity']['key']

    def _produce_ranges(self, ranges):
        prev = None
        empty = True
        for range in ranges:
            if range.get('entity'):
                yield (self._parse_col(prev), self._parse_col(range))
                prev = range
                empty = False
        yield (self._parse_col(prev), None)

    def _prepare_range_query(self, s, e):
        filters = []
        ret = { "kind" : self._kind, "filter" : { "compositeFilter" : { "op" : "AND", "filters" : filters } } }
        if s:
            filters.append({
                "propertyFilter" : {
                    "value" : {
                        "keyValue" : {
                            "partitionId" : {
                                "namespaceId" : "murer", "projectId" : "frotanetappdevel"
                            },
                            "path" : s['path']
                        }
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
                        "keyValue" : {
                            "partitionId" : {
                                "projectId" : "frotanetappdevel", "namespaceId" : "murer"
                            },
                            "path" : e['path']
                        }
                    }
                }
            })
        return ret

    def execute(self):
        with io.jreader(self._range_file, self._range_file_gz) as f:
            self._header = next(f)
            self._kind = self._header['queries'][0]['kind']
            queries = []
            for idx, ses in enumerate(blockify(self._produce_ranges(f), 3)):
                queries = [self._prepare_range_query(s, e) for s, e in ses]
                print('q', len(queries))
                output_file = os.path.join(self._output, 'part-%s' % (idx))
                print(output_file, self._kind[0]['name'], self._header['dataset'], self._header['namespace'])
                dsutil.download(
                    dataset=self._header['dataset'],
                    namespace=self._header['namespace'],
                    file=output_file,
                    file_gz=None,
                    gql=None,
                    query=queries,
                    kind=None,
                    resume=None,
                    resume_gz=None,
                    append=True
                )

def cmd_scatter():
    Scatter(
        config.args.range_file,
        config.args.range_file_gz,
        config.args.output
    ).execute()

subparser = config.add_parser('scatter', cmd_scatter)
group = subparser.add_mutually_exclusive_group(required=True)
group.add_argument('-b', '--range-file', help='input file or - for stdin')
group.add_argument('-bgz', '--range-file-gz', help='input gzip file')
subparser.add_argument('-c', '--col', default='__key__', help='column')
group = subparser.add_mutually_exclusive_group(required=True)
group.add_argument('-d', '--output', help='output directory')
group.add_argument('-dgz', '--output-gz', help='output gzip directory')
