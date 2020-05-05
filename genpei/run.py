#!/usr/bin/env python3
# coding: utf-8
import json
import multiprocessing as mp
import os
import sys
from datetime import datetime
from multiprocessing.context import BaseContext
from multiprocessing.process import BaseProcess
from pathlib import Path
from typing import Dict, List, Optional

from cwltool.main import run as cwltool_run
from flask import abort
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from genpei.const import DATE_FORMAT, FILE_NAMES
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
    run_request_file = run_dir.joinpath(FILE_NAMES["run_request"])
    with run_request_file.open(mode="w") as f:
        f.write(json.dumps(run_request, indent=2))


def prepare_exe_dir(run_id: str,
                    request_files: Dict[str, FileStorage]) \
        -> None:
    run_dir: Path = get_run_dir(run_id)
    exe_dir: Path = run_dir.joinpath(FILE_NAMES["exe_dir"])
    exe_dir.mkdir(parents=True, exist_ok=True)
    for file in request_files.values():
        if file.filename != "":
            filename: str = secure_filename(file.filename)
            file.save(exe_dir.joinpath(filename))  # type: ignore


def dump_wf_params(run_id: str, run_request: RunRequest) -> None:
    run_dir: Path = get_run_dir(run_id)
    run_dir.mkdir(parents=True, exist_ok=True)
    with run_dir.joinpath(FILE_NAMES["wf_params"]).open(mode="w") as f:
        f.write(run_request["workflow_params"])


def set_state(run_id: str, state: State) -> None:
    run_dir: Path = get_run_dir(run_id)
    run_dir.mkdir(parents=True, exist_ok=True)
    with run_dir.joinpath(FILE_NAMES["state"]).open(mode="w") as f:
        f.write(state.name)


def flatten_wf_engine_params(wf_engine_params: str) -> List[str]:
    wf_engine_params_obj = json.loads(wf_engine_params)
    params: List[str] = []
    for key, val in wf_engine_params_obj.items():
        params.append(key)
        if isinstance(val, list):
            params.append(",".join(val))
        else:
            try:
                params.append(str(val))
            except Exception:
                pass  # TODO Error Handling

    return params


def write_start_time(run_id: str) -> None:
    run_dir: Path = get_run_dir(run_id)
    run_dir.mkdir(parents=True, exist_ok=True)
    with run_dir.joinpath(FILE_NAMES["start_time"]).open(mode="w") as f:
        f.write(datetime.now().strftime(DATE_FORMAT))


def write_end_time(run_id: str) -> None:
    run_dir: Path = get_run_dir(run_id)
    run_dir.mkdir(parents=True, exist_ok=True)
    with run_dir.joinpath(FILE_NAMES["end_time"]).open(mode="w") as f:
        f.write(datetime.now().strftime(DATE_FORMAT))


def write_pid(run_id: str, pid: int) -> None:
    run_dir: Path = get_run_dir(run_id)
    run_dir.mkdir(parents=True, exist_ok=True)
    with run_dir.joinpath(FILE_NAMES["pid"]).open(mode="w") as f:
        f.write(str(pid))


def write_exit_code(run_id: str, exit_code: int) -> None:
    run_dir: Path = get_run_dir(run_id)
    run_dir.mkdir(parents=True, exist_ok=True)
    with run_dir.joinpath(FILE_NAMES["exit_code"]).open(mode="w") as f:
        f.write(str(exit_code))


def fork_run(run_id: str, run_request: RunRequest) -> None:
    ctx: BaseContext = mp.get_context("spawn")
    process: BaseProcess = \
        ctx.Process(target=forked_process, args=(run_id, run_request))
    process.start()  # Non blocking


def forked_process(run_id: str, run_request: RunRequest) -> None:
    try:
        set_state(run_id, State.INITIALIZING)
        wf_engine_params: List[str] = \
            flatten_wf_engine_params(run_request["workflow_engine_parameters"])
        wf_url: str = run_request["workflow_url"]
        wf_params_file: Path = \
            get_run_dir(run_id).joinpath(FILE_NAMES["wf_params"])
        run_dir: Path = get_run_dir(run_id)
        os.chdir(run_dir.joinpath(FILE_NAMES["exe_dir"]))
        ctx: BaseContext = mp.get_context("spawn")
        process: BaseProcess = ctx.Process(target=run_cwltool,
                                           args=(
                                               run_id,
                                               wf_engine_params,
                                               wf_url,
                                               wf_params_file
                                           ))
        set_state(run_id, State.RUNNING)
        write_start_time(run_id)
        process.start()
        pid: Optional[int] = process.pid
        if pid is not None:
            write_pid(run_id, pid)
        process.join()  # blocking
        write_end_time(run_id)
        exit_code: Optional[int] = process.exitcode
        if exit_code is not None:
            write_exit_code(run_id, exit_code)
        if exit_code == 0:
            set_state(run_id, State.COMPLETE)
        else:
            set_state(run_id, State.EXECUTOR_ERROR)
    except Exception:
        set_state(run_id, State.SYSTEM_ERROR)


def run_cwltool(run_id: str,
                wf_engine_params: List[str],
                wf_url: str,
                wf_params_file: Path) -> None:
    run_dir: Path = get_run_dir(run_id)
    sys.stdout = \
        run_dir.joinpath(FILE_NAMES["stdout"]).open(mode="w", buffering=1)
    sys.stderr = \
        run_dir.joinpath(FILE_NAMES["stderr"]).open(mode="w", buffering=1)
    cwltool_run(*wf_engine_params, wf_url, str(wf_params_file))
