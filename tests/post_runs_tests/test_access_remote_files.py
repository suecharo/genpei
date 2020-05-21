#!/usr/bin/env python3
# coding: utf-8
import json
from argparse import Namespace
from pathlib import Path
from time import sleep
from typing import Dict, Union

from flask import Flask
from flask.testing import FlaskClient
from flask.wrappers import Response
from py._path.local import LocalPath

from genpei.app import create_app, handle_default_params, parse_args
from genpei.type import RunId, RunLog, RunRequest, RunStatus

from ..resource_list import REMOTE_CWL_WF_REMOTE, REMOTE_FQ_1, REMOTE_FQ_2


def access_remote_files(client: FlaskClient) -> Response:  # type: ignore
    data: RunRequest = {  # type: ignore
        "workflow_params": json.dumps({
            "fastq_1": {
                "class": "File",
                "location": REMOTE_FQ_1
            },
            "fastq_2": {
                "class": "File",
                "location": REMOTE_FQ_2
            }
        }),
        "workflow_type": "CWL",
        "workflow_type_version": "v1.0",
        "tags": json.dumps({
            "workflow_name": "trimming_and_qc_remote"  # type: ignore
        }),
        "workflow_engine_parameters": json.dumps({}),
        "workflow_url": REMOTE_CWL_WF_REMOTE
    }
    response: Response = client.post("/runs", data=data,
                                     content_type="multipart/form-data")

    return response


def test_access_remote_files(delete_env_vars: None, tmpdir: LocalPath) -> None:
    args: Namespace = parse_args(["--run-dir", str(tmpdir)])
    params: Dict[str, Union[str, int, Path]] = handle_default_params(args)
    app: Flask = create_app(params)
    app.debug = params["debug"]  # type: ignore
    app.testing = True
    client: FlaskClient[Response] = app.test_client()
    posts_res: Response = access_remote_files(client)
    posts_res_data: RunId = posts_res.get_json()

    assert posts_res.status_code == 200
    assert "run_id" in posts_res_data

    run_id: str = posts_res_data["run_id"]
    from ..test_get_run_id_status import get_run_id_status
    count: int = 0
    while count <= 60:
        get_status_res: Response = get_run_id_status(client, run_id)
        get_status_data: RunStatus = get_status_res.get_json()
        if get_status_data["state"] == "COMPLETE":  # type: ignore
            break
        sleep(1)
        count += 1

    from ..test_get_run_id import get_run_id
    detail_res: Response = get_run_id(client, run_id)
    detail_res_data: RunLog = detail_res.get_json()

    print(detail_res_data)

    assert detail_res.status_code == 200
    assert "ERR034597_1.small.fq.trimmed.1P.fq" in detail_res_data["outputs"]
    assert "ERR034597_1.small.fq.trimmed.1U.fq" in detail_res_data["outputs"]
    assert "ERR034597_1.small.fq.trimmed.2P.fq" in detail_res_data["outputs"]
    assert "ERR034597_1.small.fq.trimmed.2U.fq" in detail_res_data["outputs"]
    assert "ERR034597_1.small_fastqc.html" in detail_res_data["outputs"]
    assert "ERR034597_2.small_fastqc.html" in detail_res_data["outputs"]
    assert "CWL" == detail_res_data["request"]["workflow_type"]
    assert "v1.0" == detail_res_data["request"]["workflow_type_version"]
    assert REMOTE_CWL_WF_REMOTE == \
        detail_res_data["request"]["workflow_url"]
    assert run_id == detail_res_data["run_id"]
    assert detail_res_data["run_log"]["exit_code"] == 0
    assert "Final process status is success" in \
        detail_res_data["run_log"]["stderr"]
    assert "COMPLETE" == detail_res_data["state"]  # type: ignore
