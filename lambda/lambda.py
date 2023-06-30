import json
import chdb

def lambda_handler(event, context):
    query = event['query'] or "SELECT version()"
    format = event['default_format'] or "JSONCompact"
    res = chdb.query(query, format)
    out = json.loads(res.data())
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(out)
    }
