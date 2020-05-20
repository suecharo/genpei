#!/usr/bin/env python3
# coding: utf-8
import multiprocessing as mp
import os
import signal
import time
from datetime import datetime
from multiprocessing.context import BaseContext
from multiprocessing.process import BaseProcess
from pathlib import Path
from traceback import print_exc
from typing import Dict, List, Optional

from cwltool.main import run as cwltool
from flask import abort
from flask.globals import current_app
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from genpei.const import CANCEL_TIMEOUT, DATE_FORMAT
from genpei.type import Log, RunLog, RunRequest, ServiceInfo, State
from genpei.util import (flatten_wf_engine_params, get_all_run_ids,
                         get_outputs, get_path, get_state, read_file,
                         read_service_info, write_file)


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


def prepare_exe_dir(run_id: str,
                    request_files: Dict[str, FileStorage]) -> None:
    exe_dir: Path = get_path(run_id, "exe_dir")
    exe_dir.mkdir(parents=True, exist_ok=True)
    for file in request_files.values():
        if file.filename != "":
            file_name: str = secure_filename(file.filename)
            file_path: Path = exe_dir.joinpath(file_name).resolve()
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file.save(file_path)  # type: ignore


def fork_run(run_id: str, run_request: RunRequest) -> None:
    run_base_dir: Path = current_app.config["RUN_DIR"]
    ctx: BaseContext = mp.get_context("spawn")
    process: BaseProcess = \
        ctx.Process(target=forked_process,
                    args=(run_id, run_request, run_base_dir,
                          current_app.config["SERVICE_INFO"]))
    process.start()  # Non blocking


def forked_process(run_id: str, run_request: RunRequest,
                   run_base_dir: Path, service_info_path: Path) -> None:
    try:
        write_file(run_id, "state", State.INITIALIZING.name, run_base_dir)
        wf_engine_params: List[str] = \
            flatten_wf_engine_params(run_request["workflow_engine_parameters"],
                                     service_info_path)
        if "--outdir" not in wf_engine_params:
            wf_engine_params.append("--outdir")
            wf_engine_params.append(
                str(get_path(run_id, "outputs_dir", run_base_dir)))
        wf_url: str = run_request["workflow_url"]
        wf_params_file: Path = get_path(run_id, "wf_params", run_base_dir)
        all_args: List[str] = [*wf_engine_params, wf_url, str(wf_params_file)]
        write_file(run_id, "cmd",
                   " ".join(["cwltool", *all_args]), run_base_dir)
        os.chdir(get_path(run_id, "exe_dir", run_base_dir))
        ctx: BaseContext = mp.get_context("spawn")
        process: BaseProcess = \
            ctx.Process(target=run_cwltool,
                        args=(run_id, all_args, run_base_dir))
        write_file(run_id, "state", State.RUNNING.name, run_base_dir)
        write_file(run_id, "start_time", datetime.now().strftime(DATE_FORMAT),
                   run_base_dir)
        process.start()
        pid: Optional[int] = process.pid
        if pid is not None:
            write_file(run_id, "pid", str(pid), run_base_dir)
        process.join()  # blocking
        write_file(run_id, "end_time", datetime.now().strftime(DATE_FORMAT),
                   run_base_dir)
        exit_code: Optional[int] = process.exitcode
        if exit_code is not None:
            write_file(run_id, "exit_code", str(exit_code), run_base_dir)
        if exit_code == 0:
            write_file(run_id, "state", State.COMPLETE.name, run_base_dir)
        else:
            write_file(run_id, "state",
                       State.EXECUTOR_ERROR.name, run_base_dir)
    except Exception:
        write_file(run_id, "state", State.SYSTEM_ERROR.name, run_base_dir)
        print_exc(file=get_path(run_id, "sys_error",
                                run_base_dir).open(mode="w"))


def run_cwltool(run_id: str, all_args: List[str], run_base_dir: Path) -> None:
    cwltool(all_args,
            stdout=get_path(run_id, "stdout",
                            run_base_dir).open(mode="w", buffering=1),
            stderr=get_path(run_id, "stderr",
                            run_base_dir).open(mode="w", buffering=1))


def get_run_log(run_id: str) -> RunLog:
    run_log: RunLog = {
        "run_id": run_id,
        "request": read_file(run_id, "run_request"),
        "state": get_state(run_id).name,  # type: ignore
        "run_log": get_log(run_id),
        "task_logs": [],
        "outputs": get_outputs(run_id)
    }

    return run_log


def get_log(run_id: str) -> Log:
    str_exit_code: str = read_file(run_id, "exit_code")
    exit_code: int
    if str_exit_code == "":
        exit_code = -999
    else:
        exit_code = int(str_exit_code)

    log: Log = {
        "name": "",
        "cmd": read_file(run_id, "cmd"),
        "start_time": read_file(run_id, "start_time"),
        "end_time": read_file(run_id, "end_time"),
        "stdout": read_file(run_id, "stdout"),
        "stderr": read_file(run_id, "stderr"),
        "exit_code": exit_code
    }

    return log


def validate_run_id(run_id: str) -> None:
    all_run_ids: List[str] = get_all_run_ids()
    if run_id not in all_run_ids:
        abort(404,
              f"The run_id {run_id} you requested does not exist, " +
              "please check with GET /runs.")


def cancel_run(run_id: str) -> None:
    state: State = get_state(run_id)
    if state == State.RUNNING:
        write_file(run_id, "state", State.CANCELING.name)
        try:
            pid: int = int(read_file(run_id, "pid"))
            os.kill(pid, signal.SIGTERM)
            count: int = 0
            while count < CANCEL_TIMEOUT:
                time.sleep(1)
                count += 1
                if get_state(run_id) != State.CANCELING:
                    write_file(run_id, "state", State.CANCELED.name)
                    break
        except Exception:
            write_file(run_id, "state", State.UNKNOWN.name)
