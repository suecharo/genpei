#!/usr/bin/env python3
# coding: utf-8
from pathlib import Path
from typing import Dict

SRC_DIR: Path = Path(__file__).parent.resolve()

DEFAULT_SERVICE_INFO: Path = \
    SRC_DIR.joinpath("service-info.json").resolve()
DEFAULT_RUN_DIR = Path.cwd().parent.joinpath("run").resolve()
DEFAULT_HOST: str = "127.0.0.1"
DEFAULT_PORT: int = 8080
GET_STATUS_CODE: int = 200
POST_STATUS_CODE: int = 200
DATE_FORMAT: str = "%Y-%m-%dT%H:%M:%S"
CANCEL_TIMEOUT: int = 10

RUN_DIR_STRUCTURE: Dict[str, str] = {
    "run_request": "run_request.json",
    "state": "state.txt",
    "exe_dir": "exe",
    "outputs_dir": "outputs",
    "wf_params": "exe/workflow_params.json",
    "start_time": "start_time.txt",
    "end_time": "end_time.txt",
    "exit_code": "exit_code.txt",
    "stdout": "stdout.log",
    "stderr": "stderr.log",
    "pid": "run.pid",
    "cmd": "cmd.txt",
    "sys_error": "sys_error.log",
}
