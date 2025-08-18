from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from logging.config import dictConfig

from app.services import Services

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})


app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app, resources={r"/parse": {"origins": "http://localhost:port"}})


@app.route('/')
def doc() -> str:
    app.logger.info("doc - Got request")
    with open("web/front.html", "r") as f:
        return f.read()


@app.route("/pronounce", methods=["POST"])
@cross_origin(origin='localhost', headers=['Content-Type', 'Authorization'])
def pronounce():
    data = request.get_json()
    app.logger.info(f"/pronounce - Got request: {data}")
    services = Services(data.get('word'))
    filepath = services.pronounce()

    os.system(f'mpg123 "{filepath}"')
    os.remove(filepath)

    return jsonify({"msg": "success"})


@app.route("/search", methods=["POST"])
@cross_origin(origin='localhost', headers=['Content-Type', 'Authorization'])
def search():
    data = request.get_json()
    app.logger.info(f"/search - Got request: {data}")
    services = Services(data.get('word'))
    entries = services.fetch()
    ret = [{
        "form": e.form if hasattr(e, "form") else data.get("word"),  # use e.form if exists
        "pos": e.pos.name if hasattr(e.pos, "name") else str(e.pos),
        "romanization": e.romanization,
        "eng_tran": e.eng_tran,
        "phon_comp": {
            "onset": e.phon_comp.onset if e.phon_comp else None,
            "nucleus": e.phon_comp.nucleus if e.phon_comp else None,
            "coda": e.phon_comp.coda if e.phon_comp else None,
            "tone": e.phon_comp.tone if e.phon_comp else None
        } if e.phon_comp else None
    } for e in entries]

    return jsonify(ret)

if __name__ == "__main__":
    app.run(host='0.0.0.0')