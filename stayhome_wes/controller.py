#!/usr/bin/env python3
# coding: utf-8
import json
from pathlib import Path

from flask import Blueprint, Response
from flask.json import jsonify

from stayhome_wes.type import ServiceInfo

app_bp = Blueprint("stayhome_wes", __name__)

SRC_DIR = Path(__file__).parent.resolve()
SERVICE_INFO_JSON = SRC_DIR.joinpath("service-info.json").resolve()


@app_bp.route("/service-info", methods=["GET"])
def get_service_info() -> Response:
    with SERVICE_INFO_JSON.open(mode="r") as f:
        res_body: ServiceInfo = json.load(f)
    response: Response = jsonify(res_body)
    response.status_code = 200

    return response


@app_bp.route("/runs", methods=["GET"])
def get_runs() -> Response:
    res_body = {"msg": "Get Runs"}
    response: Response = jsonify(res_body)
    response.status_code = 200

    return response


@app_bp.route("/runs", methods=["POST"])
def post_runs() -> Response:
    res_body = {"msg": "Post Runs"}
    response: Response = jsonify(res_body)
    response.status_code = 200

    return response


@app_bp.route("/runs/<run_id>", methods=["GET"])
def get_runs_id(run_id: str) -> Response:
    res_body = {"msg": "Get Runs ID"}
    response: Response = jsonify(res_body)
    response.status_code = 200

    return response


@app_bp.route("/runs/<run_id>/cancel", methods=["POST"])
def post_runs_id_cancel(run_id: str) -> Response:
    res_body = {"msg": "Post Runs ID Cancel"}
    response: Response = jsonify(res_body)
    response.status_code = 200

    return response


@app_bp.route("/runs/<run_id>/status", methods=["GET"])
def get_runs_id_status(run_id: str) -> Response:
    res_body = {"msg": "Get Runs ID Status"}
    response: Response = jsonify(res_body)
    response.status_code = 200

    return response
