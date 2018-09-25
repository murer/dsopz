from dsopz.config import config

def cmd_query():
    return True

subparser = config.add_parser('query', cmd_query)
subparser.add_argument('-d', '--dataset', required=True, help='dataset')
subparser.add_argument('-n', '--namespace', help='namespace')
subparser.add_argument('-g', '--gql', required=True, help='gql')
subparser.add_argument('-f', '--file', help='file')
