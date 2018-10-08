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
        with io.jwriter(self.sb('scatter.json')) as f:
            f.write({'dataset': 'any', 'namespace': self.id(), 'queries': [{"kind": [{"name": "user"}]}]})
            for idx, entity in enumerate(entities):
                if idx % 2 != 0:
                    f.write({'entity':entity})


        self.xe(['scatter', '-b', self.sb('scatter.json'), '-qpf', '3', '-d', self.sb('out')])

if __name__ == '__main__':
    unittest.main()
