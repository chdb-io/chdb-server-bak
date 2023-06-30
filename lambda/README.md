# chDB on AWS Lambda

> Running chdb in a lambda function for fun a profit!

This guide is based on [this article](https://medium.com/@skalyani103/python-on-aws-lambda-using-docker-images-5740664c54ca)

## Upload Docker image on ECR and Lambda
Lambda function continers must be hosted on the AWS Elastic Container Registry.

1. Export your AWS account id in the shell or better yet, add it your ~/.bashrc or ~/.bash_profile 
```
$ export AWS_ACCOUNT_ID = <account_id>
```

2. Install the AWS CLI and configure with your AWS credentials
```
$ aws configure
```

3. Review and execute the ‘deploy.sh’ script:
```
$ ./deploy.sh
```

4. Create Lambda function and attach your ECR Image

5. Test your Lambda function:

