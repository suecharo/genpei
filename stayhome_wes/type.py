#!/usr/bin/env python3
# coding: utf-8
from enum import Enum, auto
from typing import Any, Dict, List, TypedDict


class DefaultWorkflowEngineParameter(TypedDict):
    name: str
    type: str
    default_value: str


class Log(TypedDict):
    name: str
    cmd: List[str]
    start_time: str
    end_time: str
    stdout: str
    stderr: str
    exit_code: int


class State(Enum):
    UNKNOWN = auto()
    QUEUED = auto()
    INITIALIZING = auto()
    RUNNING = auto()
    PAUSED = auto()
    COMPLETE = auto()
    EXECUTOR_ERROR = auto()
    SYSTEM_ERROR = auto()
    CANCELED = auto()
    CANCELING = auto()


class WorkflowTypeVersion(TypedDict):
    workflow_type_version: List[str]


class ServiceInfo(TypedDict):
    workflow_type_versions: Dict[str, WorkflowTypeVersion]
    supported_wes_versions: List[str]
    supported_filesystem_protocols: List[str]
    workflow_engine_versions: Dict[str, str]
    default_workflow_engine_parameters: List[DefaultWorkflowEngineParameter]
    system_state_counts: Dict[State, int]
    auth_instructions_url: str
    contact_info_url: str
    tags: Dict[str, str]


class RunStatus(TypedDict):
    run_id: str
    state: State


class RunListResponse(TypedDict):
    runs: List[RunStatus]
    next_page_token: str


class RunRequest(TypedDict):
    workflow_params: Dict[Any, Any]
    workflow_type: str
    workflow_type_version: str
    tags: Dict[str, str]
    workflow_engine_parameters: Dict[str, str]
    workflow_url: str


class RunLog(TypedDict):
    run_id: str
    request: RunRequest
    state: State
    run_log: Log
    task_logs: List[Log]
    outputs: Dict[Any, Any]


class RunId(TypedDict):
    run_id: str


class ErrorResponse(TypedDict):
    msg: str
    status_code: int
