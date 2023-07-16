import os
import select

import chdb
from flask import Flask, request

app = Flask(__name__, static_folder="public", static_url_path="")


def chdb_query_with_errmsg(query, format):
    pipe_out, pipe_in = os.pipe()
    stderr = os.dup(2)
    os.dup2(pipe_in, 2)

    # check if we have more to read from the pipe
    def more_data():
        r, _, _ = select.select([pipe_out], [], [], 0)
        return bool(r)

    # read the whole pipe
    def read_pipe():
        out = b''
        while more_data():
            out += os.read(pipe_out, 1024)

        return out.decode(encoding='utf-8', errors='strict')

    res = chdb.query(query, format)
    os.dup2(stderr, 2)

    result = res.get_memview().tobytes()
    errmsg = read_pipe()
    return result, errmsg


@app.route('/', methods=["GET"])
def clickhouse():
    query = request.args.get('query', default="", type=str)
    format = request.args.get('default_format', default="CSV", type=str)
    if not query:
        return app.send_static_file('play.html')

    result, errmsg = chdb_query_with_errmsg(query, format)
    if errmsg == '':
        return result
    else:
        return errmsg


@app.route('/', methods=["POST"])
def play():
    query = request.data
    format = request.args.get('default_format', default="CSV", type=str)
    if not query:
        return app.send_static_file('play.html')

    result, errmsg = chdb_query_with_errmsg(query, format)
    if errmsg == '':
        return result
    else:
        return errmsg


@app.errorhandler(404)
def handle_404(e):
    return app.send_static_file('play.html')


host = os.getenv('HOST', '0.0.0.0')
port = os.getenv('PORT', 8123)
app.run(host=host, port=port)
