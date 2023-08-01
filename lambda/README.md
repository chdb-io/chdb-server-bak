<a href="https://chdb.fly.dev" target="_blank">
  <img src="https://user-images.githubusercontent.com/1423657/236688026-812c5d02-ddcc-4726-baf8-c7fe804c0046.png" width=130 />
</a>

[![.github/workflows/release.yml](https://github.com/chdb-io/chdb-server/actions/workflows/release.yml/badge.svg)](https://github.com/chdb-io/chdb-server/actions/workflows/release.yml)

# chDB AWS Lambda Function

> Let's run chdb in a lambda function for fun a profit!

<br>

## Local Lambda  Test
Build and run the Lambda chdb container locally:
```
docker build -t chdb:lambda
docker run -p 9000:8080 chdb:lambda
```

Validate the API using curl
```
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" \
     -d '{"query":"SELECT version()", "default_format":"JSONCompact"}'
```

<br>

## Upload Docker image on ECR and Lambda
Lambda function containers must be hosted on the AWS Elastic Container Registry.

1. Install the AWS CLI and configure with your AWS credentials
```
$ aws configure
```

2. Review and execute the ‘deploy.sh’ script:
```
$ ./deploy.sh [--tag <value>] [--region <value>] [--profile <default>] [--no-push]
```

3. Create Lambda function and attach your ECR Image. Make sure the name and image ID match:

![image](https://github.com/chdb-io/chdb-server/assets/1423657/887894c3-35ef-4083-a4b8-29d247f1fc1c)


4. Test your Lambda function with a JSON payload:

![image](https://github.com/chdb-io/chdb-server/assets/1423657/daa26b0b-68e2-4cec-b665-5505efe99b99)

```json
{
  "query": "SELECT version();",
  "default_format": "JSONCompact"
}
```

-----

This guide is based on [this article](https://medium.com/@skalyani103/python-on-aws-lambda-using-docker-images-5740664c54ca) which contains further details and steps.

