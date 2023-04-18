from flask import Flask, request
import chdb
import os

app = Flask(__name__, static_folder="public", static_url_path="")

@app.route('/', methods=["GET"])
def clickhouse():
    query = request.args.get('query', default="", type=str)
    format = request.args.get('default_format', default="CSV", type=str)
    if not query:
        return app.send_static_file('play.html')

    res = chdb.query(query, format)
    return res.get_memview().tobytes()

@app.route('/', methods=["POST"])
def play():
    query = request.data
    format = request.args.get('default_format', default="CSV", type=str)
    if not query:
        return app.send_static_file('play.html')

    res = chdb.query(query, format)
    return res.get_memview().tobytes()

@app.errorhandler(404)
def handle_404(e):
    return app.send_static_file('play.html')

host = os.getenv('HOST', '0.0.0.0')
port = os.getenv('PORT', 8123)
app.run(host=host, port=port)
