import argparse
import processor
import sys
import json

class UpdateProcessor(processor.Processor):

    def __init__(self, props, kinds = []):
        super(UpdateProcessor, self).__init__(kinds)
        self.props = json.loads(props)

    def resolve(self):
        print >> sys.stderr, 'process', self.processed
        for ent in self.block:
            for name,value in self.props.iteritems():
                if value.get('excludeFromIndexes') == None:
                    value['excludeFromIndexes'] = True

                ent['properties'][name] = value
            print json.dumps(ent)

def argparse_prepare(sub):
    sub.add_argument('-k', '--kinds', nargs='+', help='kinds')
    sub.add_argument('-p', '--properties', required=True,  help='properties')

def argparse_exec(args):
    processor = UpdateProcessor(args.properties ,args.kinds)
    processor.process()
