#!/usr/bin/env python3
# coding: utf-8
from argparse import Namespace
from pathlib import Path
from typing import Dict, Union

from flask import Flask
from flask.testing import FlaskClient
from flask.wrappers import Response

from genpei.app import create_app, handle_default_params, parse_args
from genpei.type import ServiceInfo


def test_get_service_info(delete_env_vars: None) -> None:
    args: Namespace = parse_args([])
    params: Dict[str, Union[str, int, Path]] = handle_default_params(args)
    app: Flask = create_app(params)
    app.debug = params["debug"]  # type: ignore
    app.testing = True
    client: FlaskClient[Response] = app.test_client()
    res: Response = client.get("/service-info")
    res_data: ServiceInfo = res.get_json()

    assert res.status_code == 200
    assert "workflow_type_versions" in res_data
    assert "supported_wes_versions" in res_data
    assert "supported_filesystem_protocols" in res_data
    assert "workflow_engine_versions" in res_data
    assert "default_workflow_engine_parameters" in res_data
    assert "system_state_counts" in res_data
    assert "auth_instructions_url" in res_data
    assert "contact_info_url" in res_data
    assert "tags" in res_data
