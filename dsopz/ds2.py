
class Error(Exception):
    """Exceptions"""

class Partition(object):

    def __init__(self, dataset=None, namespace=None):
        self.dataset = dataset
        self.namespace = namespace

class Header(object):

    def __init__(self, dataset=None, namespace=None, query=[]):
        self.dataset = dataset
        self.namespace = namespace
        self.queries = []

class Key(object):

    def __init__(self, path, partition=None):
        self.path = path
        self.partition = partition

class Prop(object):

    def __init__(self, value):
        this.value = value
        this.excludeFromIndex = false

class Entity(object):

    def __init__(self, key, **kwargs):
        self.key = key
        self.properties = {}

class EntityBlockReader(object):

    def read(self):
        raise Error('abstract')

def __main():
    Entity.create(
        Key((('p1', 'v1'), ('p2', 'v2')), Partition('any', 'test')),
        p1 = StringProp('test'),
        p2 = IntProp(3)
    )

if __name__ == '__main__':
    __main()
