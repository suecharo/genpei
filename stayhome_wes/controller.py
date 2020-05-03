#!/usr/bin/env python3
# coding: utf-8
from flask import Blueprint, Response
from flask.json import jsonify

app_bp = Blueprint("stayhome_wes", __name__)


@app_bp.route("/service-info", methods=["GET"])
def get_service_info() -> Response:
    res_body = {"msg": "Hello stayhome_wes"}
    response: Response = jsonify(res_body)
    response.status_code = 200

    return response
