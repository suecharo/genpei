#!/usr/bin/env python3
# coding: utf-8
import json
from pathlib import Path
from typing import Dict, List

from flask import abort
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from genpei.const import (EXE_DIR_NAME, RUN_REQUEST_FILE_NAME, STATE_FILE_NAME,
                          WF_PARAMS_FILE_NAME)
from genpei.type import RunRequest, ServiceInfo, State
from genpei.util import get_run_dir, read_service_info


def validate_run_request(run_request: RunRequest) -> None:
    required_fields: List[str] = ["workflow_params",
                                  "workflow_type",
                                  "workflow_type_version",
                                  "workflow_url"]
    for field in required_fields:
        if field not in run_request:
            abort(400,
                  f"{field} not included in the form data of the request.")


def validate_wf_type(wf_type: str, wf_type_version: str) -> None:
    service_info: ServiceInfo = read_service_info()
    wf_type_versions = service_info["workflow_type_versions"]

    available_wf_types: List[str] = \
        list(map(str, wf_type_versions.keys()))
    if wf_type not in available_wf_types:
        abort(400,
              f"{wf_type}, the workflow_type specified in the " +
              f"request, is not included in {available_wf_types}, " +
              "the available workflow_types.")

    available_wf_versions: List[str] = \
        list(map(str, wf_type_versions[wf_type]["workflow_type_version"]))
    if wf_type_version not in available_wf_versions:
        abort(400,
              f"{wf_type_version}, the workflow_type_version specified in " +
              f"the request, is not included in {available_wf_versions}, " +
              "the available workflow_type_versions.")


def prepare_run_dir(run_id: str, run_request: RunRequest) -> None:
    run_dir: Path = get_run_dir(run_id)
    run_dir.mkdir(parents=True, exist_ok=True)
    run_request_file = run_dir.joinpath(RUN_REQUEST_FILE_NAME)
    with run_request_file.open(mode="w") as f:
        f.write(json.dumps(run_request, indent=2))


def prepare_exe_dir(run_id: str,
                    request_files: Dict[str, FileStorage]) \
        -> None:
    run_dir: Path = get_run_dir(run_id)
    exe_dir: Path = run_dir.joinpath(EXE_DIR_NAME)
    exe_dir.mkdir(parents=True, exist_ok=True)
    for file in request_files.values():
        if file.filename != "":
            filename: str = secure_filename(file.filename)
            file.save(exe_dir.joinpath(filename))  # type: ignore


def dump_wf_params(run_id: str, run_request: RunRequest) -> None:
    run_dir: Path = get_run_dir(run_id)
    run_dir.mkdir(parents=True, exist_ok=True)
    with run_dir.joinpath(WF_PARAMS_FILE_NAME).open(mode="w") as f:
        f.write(run_request["workflow_params"])


def set_state(run_id: str, state: State) -> None:
    run_dir: Path = get_run_dir(run_id)
    run_dir.mkdir(parents=True, exist_ok=True)
    with run_dir.joinpath(STATE_FILE_NAME).open(mode="w") as f:
        f.write(state.name)


def flatten_wf_engine_params(wf_engine_params: str) -> List[str]:
    wf_engine_params_obj = json.loads(wf_engine_params)
    print(wf_engine_params_obj)

    return ["TODO"]


def fork_run(run_id: str, run_request: RunRequest) -> None:
    pass


def forked_process(run_id: str, run_request: RunRequest) -> None:
    try:
        set_state(run_id, State.INITIALIZING)
        wf_engine_params: List[str] = \
            flatten_wf_engine_params(run_request["workflow_engine_parameters"])
        wf_url: str = run_request["workflow_url"]
        wf_params_file: Path = \
            get_run_dir(run_id).joinpath(WF_PARAMS_FILE_NAME)
        # TODO cd to exe dir
        set_state(run_id, State.RUNNING)
        # TODO start_time, end_time
        run_cwltool(wf_engine_params, wf_url, wf_params_file)
        set_state(run_id, State.COMPLETE)
    except Exception:
        set_state(run_id, State.SYSTEM_ERROR)


def run_cwltool(wf_engine_params: List[str], wf_url: str,
                wf_params_file: Path) -> None:
    print(wf_engine_params)
    print(wf_url)
    print(wf_params_file)
