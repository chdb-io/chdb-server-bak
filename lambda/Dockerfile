FROM public.ecr.aws/lambda/python:latest
COPY lambda.py ./
COPY requirements.txt ./
RUN python3 -m pip install -r requirements.txt

CMD ["lambda.lambda_handler"]
