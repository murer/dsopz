from dsopz.http import req_json
from dsopz.oauth import oauth

def run_query(
        dataset,
        namespace,
        gql,
        offset = None,
        limit = None,
        start_cusror = None,
        end_cursor = None):

    url = 'https://datastore.googleapis.com/v1/projects/%s:runQuery' % (dataset)
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
    print(resp)


    return [{}]
