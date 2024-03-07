from flask import Flask, jsonify, request, render_template
import traceback
from flask_cors import CORS

app = Flask(
    __name__,
    static_folder="../../frontend/dist/assets",
    template_folder="../../frontend/dist",
)
cors = CORS(app, resources={r"*": {"origins": "*"}})

# load models
MODELS = {}

# Flask config
app.config["JSON_AS_ASCII"] = False  # ban for kanji forwarded
from .config import Config
from .util import timer, get_model, model_filter, get_avilable_device, choose_device


# retune hale model information
@app.route("/api/models-info.fuck", methods=["POST"])
def model_info():
    return app.config["MODELS_CONFIG"][
        ["name", "description", "max-length", "src", "tgt"]
    ].to_json(orient="records")


# filter model with languages, not recommend to use this api
@app.route("/api/filter.fuck", methods=["POST"])
def filter():
    try:
        data = request.get_json()
        src = data["src"]
        tgt = data["tgt"]
        model = data["model"]
        result = model_filter(src=src, tgt=tgt, model=model)
        resp = {}
        resp["info"] = result[
            ["name", "description", "max-length", "src", "tgt"]
        ].to_dict(orient="records")
        resp["msg"] = "success"
        resp["coed"] = 200
        return jsonify(resp)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"msg": "bad parameter", "code": 401})


# get avilable device information
@app.route("/api/devices.fuck", methods=["POST", "GET"])
def get_devices():
    try:
        devices = get_avilable_device()
        return jsonify({"devices": devices, "code": 200, "msg": "success"})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"msg": "bad parameter", "code": 401})


# do nmt translation
@timer
@app.route("/api/nmt.fuck", methods=["POST"])
def do_nmt():
    try:
        data = request.get_json()
        input = data["text"]
        model_name = data["model"]
        src = data["src"]
        tgt = data["tgt"]
        # device = int(data["device"])
        device = data["device"]
        device = choose_device(device)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"msg": "bad parameter", "code": 401})
    try:
        assert model_name in app.config["MODELS_CONFIG"]["name"].to_list()
        model = get_model(model_name, device=device)
        output = model(input, src=src, tgt=tgt)
        return jsonify({"result": output, "code": 200, "msg": "success"})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"msg": "server error", "code": 503})


# home page
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    return render_template("index.html")


if __name__ == "__main__":
    app.run(port=5000)
