from dsopz.http import req_json
from dsopz.oauth import oauth
from dsopz.config import config

def run_query(
        dataset,
        namespace,
        gql,
        offset = None,
        limit = None,
        start_cusror = None,
        end_cursor = None):

    url = '%s/v1/projects/%s:runQuery' % (config.args.url, dataset)
    gql_full = gql
    body = {
        'partitionId': {
            'projectId': dataset,
            'namespaceId': namespace
        },
        'gqlQuery': {
            'allowLiterals': True,
            'queryString': gql_full
        }
    }
    resp = req_json('POST', url, body, {
        'Authorization': 'Bearer %s' % (oauth.access_token())
    })
    ret = resp['body']
    ret['batch']['entityResults'] = ret['batch'].get('entityResults', [])
    return ret
