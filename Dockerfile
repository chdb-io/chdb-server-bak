FROM python:3.8.10-slim
ENV VERSION 0.6.0
RUN apt update && apt install -y binutils \
  && pip install chdb Flask \
  && strip /usr/local/lib/python3.8/site-packages/chdb/_chdb.cpython-38-*-linux-gnu.so \
  && rm -rf /var/lib/apt/lists/* && rm -rf ~/.cache/pip/*
WORKDIR /app
ADD main.py .
ADD public ./public
# RUN python3 -c "import chdb; res = chdb.query('select version()', 'CSV'); print(str(res.get_memview().tobytes()))"
EXPOSE 8123
CMD ["python3","./main.py"]
