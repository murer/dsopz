from dsopz.config import config

def cmd_query():
    return True

subparser = config.add_parser('query', cmd_query)
subparser.add_argument('-d', '--dataset', required=True, help='dataset')
subparser.add_argument('-n', '--namespace', help='namespace')
group = subparser.add_mutually_exclusive_group(required=True)
group.add_argument('-g', '--gql', help='gql')
group.add_argument('-q', '--query', help='json query')
group.add_argument('-r', '--resume', help='json query and cursor from file')
group.add_argument('-rgz', '--resume-gz', help='json query and cursor from gzip file or - for stdin')
group = subparser.add_mutually_exclusive_group(required=True)
group.add_argument('-f', '--file', help='output file or - for stdout')
group.add_argument('-fgz', '--file-gz', help='output gzip file or - for stdout')

subparser = config.add_parser('kind', cmd_kind)
subparser.add_argument('-d', '--dataset', required=True, help='dataset')
subparser.add_argument('-n', '--namespace', help='namespace')
subparser.add_argument('-a', '--all', action='store_true', help='print "__.*__" also')
group = subparser.add_mutually_exclusive_group(required=True)
group.add_argument('-f', '--file', help='output file or - for stdout')
group.add_argument('-fgz', '--file-gz', help='output gzip file or - for stdout')

subparser = config.add_parser('namespace', cmd_namespace)
subparser.add_argument('-d', '--dataset', required=True, help='dataset')
group = subparser.add_mutually_exclusive_group(required=True)
group.add_argument('-f', '--file', help='output file or - for stdout')
group.add_argument('-fgz', '--file-gz', help='output gzip file or - for stdout')

subparser = config.add_parser('upsert', cmd_namespace)
subparser.add_argument('-d', '--dataset', required=True, help='dataset')
subparser.add_argument('-n', '--namespace', help='namespace')
group = subparser.add_mutually_exclusive_group(required=True)
group.add_argument('-f', '--file', help='input file or - for stdin')
group.add_argument('-fgz', '--file-gz', help='input gzip file or - for stdin')

subparser = config.add_parser('rm', cmd_namespace)
subparser.add_argument('-d', '--dataset', required=True, help='dataset')
subparser.add_argument('-n', '--namespace', help='namespace')
group = subparser.add_mutually_exclusive_group(required=True)
group.add_argument('-f', '--file', help='input file or - for stdin')
group.add_argument('-fgz', '--file-gz', help='input gzip file or - for stdin')
