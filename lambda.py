import os
import json
import chdb
        
def lambda_handler(event, context):
    json_region = os.environ['AWS_REGION']
    query = event['query'] or "SELECT version()"
    format = event['default_format'] or "JSONCompact"
    res = chdb.query(query, format)
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(res.get_memview().tobytes())
    }
