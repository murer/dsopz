from dsopz import io
import unittest
from dsopztest import abstract_test_case
from dsopz import datastore as ds
import json as JSON

class CmdscatterTest(abstract_test_case.TestCase):

    def test_scatter(self):
        entities = [
            ds.centity(ds.ckey(('hero', 'a%s' % (i)))) for i in range(9)
        ]
        ds.mutation('any', self.id(), upserts=entities)
        with io.jwriter(gz=self.sb('scatter.json.gz')) as gz:
            with io.jwriter(self.sb('scatter.json')) as f:
                header = {'dataset': 'any', 'namespace': self.id(), 'queries': [{"kind": [{"name": "hero"}]}]}
                f.write(header)
                gz.write(header)
                for idx, entity in enumerate(entities):
                    if idx % 2 != 0:
                        f.write({'entity':entity})
                        gz.write({'entity':entity})

        self.xe(['scatter', '-b', self.sb('scatter.json'), '-qpf', '3', '-d', self.sb('out')])
        result = io.read_all(plain=self.sb('out/part-0'))
        result.pop(0)
        self.assertEqual(['a0', 'a1', 'a2', 'a3', 'a4'], [ent['entity']['key']['path'][0]['name'] for ent in result] )
        result = io.read_all(plain=self.sb('out/part-1'))
        result.pop(0)
        self.assertEqual(['a5', 'a6', 'a7', 'a8'], [ent['entity']['key']['path'][0]['name'] for ent in result] )

        self.xe(['scatter', '-bgz', self.sb('scatter.json.gz'), '-qpf', '3', '-dgz', self.sb('outgz')])
        result = io.read_all(plain=self.sb('out/part-0'))
        result.pop(0)
        self.assertEqual(['a0', 'a1', 'a2', 'a3', 'a4'], [ent['entity']['key']['path'][0]['name'] for ent in result] )
        result = io.read_all(plain=self.sb('out/part-1'))
        result.pop(0)
        self.assertEqual(['a5', 'a6', 'a7', 'a8'], [ent['entity']['key']['path'][0]['name'] for ent in result] )

if __name__ == '__main__':
    unittest.main()
