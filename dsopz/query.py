
class Query(object):

    def __init__(self,
            dataset,
            namespace,
            gql,
            offset = None,
            limit = None,
            start_cusror = None,
            end_cursor = None):
        self.dataset = dataset
        self.namespace = namespace
        self.gql = gql
        self.offset = offset
        self.limit = limit
        self.start_cusror = start_cusror
        self.end_cursor = end_cursor

    def execute(self):
        return [{}]
