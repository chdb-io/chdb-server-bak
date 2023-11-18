import os
import sys
import tempfile
import hashlib

import chdb
from chdb import session as chs
from flask import Flask, request
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__, static_folder="public", static_url_path="")
auth = HTTPBasicAuth()
driver = chdb

# session support: basic username + password as unique datapath
@auth.verify_password
def verify(username, password):
    if not (username and password):
        # print('stateless session')
        globals()["driver"] = chdb
    else:
        hash = hashlib.md5(str(username + password).encode('utf-8')).hexdigest()
        path = globals()["path"] + "/" + str(hash)
        # print('stateful session ' + path)
        globals()["driver"] = chs.Session(path)
    return True

# run chdb.query(query, format), get result from return and collect stderr
def chdb_query_with_errmsg(query, format, data=None):
    output = ""
    errmsg = ""
    try:
        stderr_tempfile = tempfile.TemporaryFile()
        old_stderr_fd = os.dup(2)
        os.dup2(stderr_tempfile.fileno(), 2)

        if data is not None and query is not None:
            stdin_tempfile = tempfile.NamedTemporaryFile()
            # print(stdin_tempfile.name)
            old_stdin_fd = os.dup(0)
            os.dup2(stdin_tempfile.fileno(), 0)
            stdin_tempfile.write(data)
            stdin_tempfile.seek(0)

        output = driver.query(query, format).bytes()

        stderr_tempfile.flush()
        stderr_tempfile.seek(0)
        errmsg = stderr_tempfile.read()

    except Exception as e:
        errmsg = str(e)

    finally:
        os.dup2(old_stderr_fd, 2)
        stderr_tempfile.close()
        if data is not None:
            os.dup2(old_stdin_fd, 0)
            stdin_tempfile.close()

    return output, errmsg

@app.route('/', methods=["GET"])
@auth.login_required
def clickhouse():
    query = request.args.get('query', default="", type=str)
    format = request.args.get('default_format', default="TSV", type=str)
    database = request.args.get('database', default="", type=str)
    if not query:
        return app.send_static_file('play.html')

    if database:
        use = f"USE {database};".encode()
        chdb_query_with_errmsg(use.strip(), format)

    result, errmsg = chdb_query_with_errmsg(query.strip(), format)
    if len(errmsg) == 0:
        return result, 200
    elif len(result) > 0:
        print("warning:", errmsg)
        return result, 200
    else:
        print("error:", errmsg)
        return errmsg, 400

@app.route('/', methods=["POST"])
@auth.login_required
def play():
    query = request.args.get('query', default=None, type=str)
    body = request.get_data() or None
    format = request.args.get('default_format', default="TSV", type=str)
    database = request.args.get('database', default="", type=str)
    data = None

    if query is None:
        if body is not None:
            query = body
            body = None
        else:
            query = b""
    else:
        query = query.encode('utf-8')

    if body is not None:
        if query is None:
            query = body # body.encode('utf-8')
        else:
            data = body

    if not query and not body:
        return "Error: no query parameter provided", 400

    if database:
        use = f"USE {database};".encode()
        chdb_query_with_errmsg(use.strip(), format)

    result, errmsg = chdb_query_with_errmsg(query.strip(), format, data)
    if len(errmsg) == 0:
        return result, 200
    if len and len(result) > 0:
        print("warning:", errmsg)
        return result, 200
    else:
        return errmsg, 400


@app.route('/play', methods=["GET"])
def handle_play():
    return app.send_static_file('play.html')

@app.route('/ping', methods=["GET"])
def handle_ping():
    return "Ok", 200

@app.errorhandler(404)
def handle_404(e):
    return app.send_static_file('play.html')

host = os.getenv('HOST', '0.0.0.0')
port = os.getenv('PORT', 8123)
path = os.getenv('DATA', '.chdb_data')
app.run(host=host, port=port)
