import json
from flask import jsonify

def jsonify_wrapper_mongo_engine(data):
    return jsonify(json.loads(data.to_json()))