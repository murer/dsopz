from dsopz import datastore as api
class Error(Exception):
    """Exceptions"""

class Partition(object):

    def __init__(self, dataset, namespace=None):
        self.dataset = dataset
        self.namespace = namespace

    def format(self):
        ret = {'projectId': self.dataset}
        if self.namespace:
            ret['namespaceId'] = self.namespace
        return ret

class Header(object):

    def __init__(self, dataset=None, namespace=None, queries=[]):
        self.dataset = dataset
        self.namespace = namespace
        self.queries = []

class Key(object):

    def __init__(self, kind, name, parent=None, partition=None):
        self.kind = kind
        self.name = name
        self.parent = None
        self.partition = partition

    def format(self):
        keys = [self]
        while keys[0].parent:
            if keys.parent.partition:
                raise Error('wrong')
            keys = [k] + keys
        print('keys', keys)
        ret = { 'path': [{
            'kind': k.kind,
            'id' if k.name == None or isinstance(k.name, int) else 'name': k.name
        } for k in keys] }
        if self.partition:
            ret['partition'] = self.partition.format()
        return ret

class Prop(object):

    def __init__(self, value):
        self.value = value
        self.excludeFromIndexes = False

    def format(self):
        ret = self.format_value()
        ret['excludeFromIndexes'] = self.excludeFromIndexes
        return ret

class StringProp(Prop):

    def format_value(self):
        return { 'stringValue': self.value }

class Entity(object):

    def __init__(self, key, props):
        self.key = key
        self.properties = props

    def format(self):
        return {
            'key': self.key.format(),
            'properties': format(self.properties)
        }

def format_dict(obj):
    ret = {}
    print('xxxx211', obj)
    for k, v in obj.items():
        print('xxxx', k, v)
        ret[k] = format(v)
    return ret

def format(obj):
    if isinstance(obj, dict):
        return format_dict(obj)
    if isinstance(obj, list):
        return [format(k) for k in obj]
    return obj.format()

def parse(line):
    return

class Datastore(object):

    def __init__(self, dataset, namespace):
        self.dataset = dataset
        self.namespace = namespace

    def _set_partition(self, target):
        key = target.get('key', target)
        key['partitionId'] = Partition(self.dataset, self.namespace).format()
        return target

    def put(self, entities):
        entities = format(entities)
        mutations = {
            'mode': 'NON_TRANSACTIONAL',
            'mutations': [
                { 'upsert': self._set_partition(entity) } for entity in entities
            ]
        }
        print('mutations', mutations)
        result = api.commit(self.dataset, self.namespace, mutations)
        print('result', result)
        return result

    def get(keys):
        return

    def delete(keys):
        return

    def query(query):
        return

def __main():
    """ aaa """

if __name__ == '__main__':
    __main()
