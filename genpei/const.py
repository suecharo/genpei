#!/usr/bin/env python3
# coding: utf-8
from typing import Dict

DEFAULT_HOST: str = "0.0.0.0"
DEFAULT_PORT: int = 8080
GET_STATUS_CODE: int = 200
POST_STATUS_CODE: int = 200

FILE_NAMES: Dict[str, str] = {
    "service_info": "service-info.json",
    "run_request": "run_request.json",
    "state": "state.txt",
    "exe_dir": "exe",
    "wf_params": "workflow_params.json",
    "start_time": "start_time.txt",
    "end_time": "end_time.txt",
    "exit_code": "exit_code.txt",
    "stdout": "stdout.log",
    "stderr": "stderr.log",
    "pid": "run.pid"
}

DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"
