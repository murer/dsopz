from sys import modules as _modules
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

    @staticmethod
    def parse(obj):
        if not obj:
            return None
        return Partition(obj['projectId'], obj.get('namespaceId'))

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
            ret['partitionId'] = self.partition.format()
        return ret

    @staticmethod
    def parse(obj):
        if not obj:
            return None
        partition = Partition.parse(obj.get('partition'))
        key = None
        for path in obj['path']:
            key = Key(
                path['kind'],
                path.get('id') if isinstance(path.get('id'), int) else path.get('name'),
                parent=key
            )
        if partition:
            key.partition = partition
        print('xxxx', key)
        return key

class Prop(object):

    def __init__(self, value, excludeFromIndexes=False):
        self.value = value
        self.excludeFromIndexes = excludeFromIndexes

    def format(self):
        name = self.__class__.__name__
        print('PPPPPP', name)
        name = '%s%s%s' % (name[0].lower(), name[1:-4], 'Value')
        print('PPPPPP2', name)
        return {
            name: self.format_value(),
            'excludeFromIndexes': self.excludeFromIndexes
        }

    @staticmethod
    def can_parse(obj):
        for p in obj:
            if p.endswith('Value'):
                return True
        return False

    @staticmethod
    def parse(obj):
        for p in obj:
            if p.endswith('Value'):
                name = '%s%s' %(p[0:-5].title(), 'Prop')
                print('name', name, __name__)
                current_module = _modules[__name__]
                print('mmm', current_module)
                clazz = getattr(current_module, name)
                print('clazz', clazz)
                value = clazz.parse_value(obj[p])
                print('value', value)
                excludeFromIndexes = obj.get('excludeFromIndexes', False)
                print('excludeFromIndexes', excludeFromIndexes)
                return clazz(value, excludeFromIndexes)

class StringProp(Prop):

    def format_value(self):
        return self.value

    @staticmethod
    def parse_value(obj):
        return obj

class Entity(object):

    def __init__(self, key, props):
        self.key = key
        for p, v in props.items():
            if not isinstance(v, Prop):
                raise Error('wrong %s=%s' % (p, type(v)))
        self.properties = props

    def format(self):
        return {
            'key': self.key.format(),
            'properties': format(self.properties)
        }

    @staticmethod
    def parse(obj):
        key = Key.parse(obj['key'])
        props = {}
        print('UUU2', key)
        for p, v in obj.get('properties', {}).items():
            print('p,v', p, v)
            props[p] = parse(v)
        return Entity(key, props)

class EntityResult(object):

    def __init__(self, entity):
        self.entity = entity

    def format(self):
        ret = {}
        if self.entity:
            ret['entity'] = format(self.entity)
        return ret

    @staticmethod
    def parse(obj):
        entity = Entity.parse(obj.get('entity'))
        return EntityResult(entity)

def format_dict(obj):
    ret = {}
    print('xxxx211', obj)
    for k, v in obj.items():
        print('xxxx', k, v)
        ret[k] = format(v)
    return ret

def format(obj):
    if obj == None:
        return None
    if isinstance(obj, dict):
        return format_dict(obj)
    if isinstance(obj, list):
        return [format(k) for k in obj]
    return obj.format()

def parse(obj):
    if isinstance(obj, list):
        return [parse(k) for k in obj]
    if not isinstance(obj, dict):
        raise Error('unknown: %s' % (type(obj)))
    if obj.get('entity'):
        return EntityResult.parse(obj)
    if Prop.can_parse(obj):
        return Prop.parse(obj)
    raise Error('unknown: %s' % obj)

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

    def get(self, keys):
        akeys = format(keys)
        if isinstance(keys, Key):
            akeys = [ akeys ]
        print('akeys', akeys)
        aresult = api.lookup(self.dataset, self.namespace, akeys)
        print ('aresult', aresult)
        result = parse(aresult)
        print ('result', result)
        print ('xresult', format(result))
        return

    def delete(self, keys):
        return

    def query(self, query):
        return

def __main():
    """ aaa """

if __name__ == '__main__':
    __main()
