import os
import tempfile

import chdb
from flask import Flask, request

app = Flask(__name__, static_folder="public", static_url_path="")


# run chdb.query(query, format), get result from return and collect stderr
def chdb_query_with_errmsg(query, format):
    # Redirect stdout and stderr to the buffers
    try:
        new_stderr = tempfile.TemporaryFile()
        old_stderr_fd = os.dup(2)
        os.dup2(new_stderr.fileno(), 2)
        # Call the function
        output = chdb.query(query, format).bytes()
        
        new_stderr.flush()
        new_stderr.seek(0)
        errmsg = new_stderr.read()
        
        # cleanup and recover
        new_stderr.close()
        os.dup2(old_stderr_fd, 2)
    except Exception as e:
        # An error occurred, print it to stderr
        print(f"An error occurred: {e}")
    return output, errmsg
    

@app.route('/', methods=["GET"])
def clickhouse():
    query = request.args.get('query', default="", type=str)
    format = request.args.get('default_format', default="CSV", type=str)
    if not query:
        return app.send_static_file('play.html')

    result, errmsg = chdb_query_with_errmsg(query, format)
    if len(errmsg) == 0:
        return result
    return errmsg


@app.route('/', methods=["POST"])
def play():
    query = request.data
    format = request.args.get('default_format', default="CSV", type=str)
    if not query:
        return app.send_static_file('play.html')

    result, errmsg = chdb_query_with_errmsg(query, format)
    if len(errmsg) == 0:
        return result
    return errmsg


@app.errorhandler(404)
def handle_404(e):
    return app.send_static_file('play.html')


host = os.getenv('HOST', '0.0.0.0')
port = os.getenv('PORT', 8123)
app.run(host=host, port=port)
