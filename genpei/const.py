#!/usr/bin/env python3
# coding: utf-8
from typing import Dict

DEFAULT_HOST: str = "0.0.0.0"
DEFAULT_PORT: int = 8080
GET_STATUS_CODE: int = 200
POST_STATUS_CODE: int = 200

RUN_DIR_STRUCTURE: Dict[str, str] = {
    "service_info": "service-info.json",
    "run_request": "run_request.json",
    "state": "state.txt",
    "exe": "exe",
    "output": "output",
    "wf_params": "exe/workflow_params.json",
    "start_time": "start_time.txt",
    "end_time": "end_time.txt",
    "exit_code": "exit_code.txt",
    "stdout": "stdout.log",
    "stderr": "stderr.log",
    "pid": "run.pid",
    "cmd": "cmd.txt",
    "sys_error": "sys_error.log"
}

DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"
