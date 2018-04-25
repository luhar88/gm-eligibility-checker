import os
import json
import importlib

from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException, default_exceptions, NotFound, BadRequest, InternalServerError

V1_PATH = '/v1/%s'
UNKNOWN_ERROR = 'Oops something went wrong!'
PARTNER_LIST_FILE = os.path.join('web', 'sample_data', 'partner_metadata.json')
PARTNER_MODULES = 'web.libs.%s'


def json_app(app):
    def error_handling(error):
        if isinstance(error, HTTPException):
            result = {
                'code': error.code,
                'message': error.description
            }
        else:
            result = {
                'code': 500,
                'message': UNKNOWN_ERROR
            }
        resp = jsonify(result)
        resp.status_code = result['code']
        return resp

    for code in default_exceptions.keys():
        app.register_error_handler(code, error_handling)

    return app


app = json_app(Flask(__name__))


with open(PARTNER_LIST_FILE, 'r') as f:
    partners = json.load(f)


@app.route(V1_PATH % 'ping', methods=['GET'])
def ping():
    return jsonify('pong')


@app.route(V1_PATH % '<partner_id>/config', methods=['GET'])
def get_config(partner_id):
    partner_md = partners.get(partner_id)

    if partner_md:
        _module = importlib.import_module(PARTNER_MODULES % partner_md.get('module'))
        _class = getattr(_module, partner_md.get('class'))

        pec = _class(partner_id)
        config = pec.config()

        return jsonify({'schema': config})
    else:
        raise NotFound(description='unknown partner')


@app.route(V1_PATH % '<partner_id>/check', methods=['POST'])
def check_eligibility(partner_id):
    if not request.json:
        raise BadRequest(description='Invalid req data format, check schema at /v1/config')

    partner_md = partners.get(partner_id)

    if partner_md:
        _module = importlib.import_module(PARTNER_MODULES % partner_md.get('module'))
        _class = getattr(_module, partner_md.get('class'))

        pec = _class(partner_id)
        result = pec.check_eligibility(data=request.get_json())

        if result[0] == 'success':
            return jsonify(result[1])
        elif result[0] == 'invalid_schema':
            raise BadRequest(description='Invalid Schema')
        else:
            raise InternalServerError(description=UNKNOWN_ERROR)

    else:
        raise NotFound(description='unknown partner')


@app.route('/')
@app.route('/<path:path>')
def catch_all(path=None):
    raise NotFound(description='Route not found!')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False, port=8000)
