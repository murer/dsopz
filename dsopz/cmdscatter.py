from dsopz.config import config
from dsopz import io
from dsopz import dsutil
from dsopz.datastore import stream_block, mutation, stream_entity
from dsopz.processor import blockify, merge_gens, AsyncGen, dispatch
from dsopz import util
import logging as log
import json as JSON

class Error(Exception):
    """Exceptions"""

class Scatter(object):

    def __init__(self, block_file, block_file_gz):
        self.block_file = block_file
        self.block_file_gz = block_file_gz

    def _parse_col(self, line):
        if not line:
            return None
        return line['entity']['key']

    def _produce_blocks(self, blocks):
        prev = None
        empty = True
        for block in blocks:
            if block.get('entity'):
                yield (self._parse_col(prev), self._parse_col(block))
                prev = block
                empty = False
        yield (self._parse_col(prev), None)

    def _prepare_block_query(self, s, e):
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
        with io.jreader(self.block_file, self.block_file_gz) as f:
            self._header = next(f)
            self._kind = self._header['queries'][0]['kind']
            for s, e in self._produce_blocks(f):
                query = self._prepare_block_query(s, e)
                print('q', query)

def cmd_scatter():
    Scatter(config.args.block_file, config.args.block_file_gz).execute()

subparser = config.add_parser('scatter', cmd_scatter)
group = subparser.add_mutually_exclusive_group(required=True)
group.add_argument('-b', '--block-file', help='input file or - for stdin')
group.add_argument('-bgz', '--block-file-gz', help='input gzip file')
subparser.add_argument('-c', '--col', default='__key__', help='column')
group = subparser.add_mutually_exclusive_group(required=True)
group.add_argument('-d', '--dir', help='output directory')
group.add_argument('-dgz', '--dir-gz', help='output gzip directory')
