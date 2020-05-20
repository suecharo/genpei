#!/usr/bin/env python3
# coding: utf-8
import collections
import json
import os
import shlex
from pathlib import Path
from traceback import format_exc
from typing import Any, Dict, Iterable, List, Optional
from uuid import uuid4

from cwltool.update import ALLUPDATES
from cwltool.utils import versionstring
from flask import current_app

from genpei.const import RUN_DIR_STRUCTURE
from genpei.type import DefaultWorkflowEngineParameter, ServiceInfo, State

CWLTOOL_VERSION: str = versionstring().split(" ")[1]
CWL_VERSIONS: List[str] = list(map(str, ALLUPDATES.keys()))


def read_service_info(service_info_path: Optional[Path] = None) -> ServiceInfo:
    if service_info_path is None:
        service_info_path = current_app.config["SERVICE_INFO"]
    with service_info_path.open(mode="r") as f:
        service_info: ServiceInfo = json.load(f)
    service_info["workflow_engine_versions"]["cwltool"] = CWLTOOL_VERSION
    service_info["workflow_type_versions"]["CWL"]["workflow_type_version"] = \
        CWL_VERSIONS
    service_info["system_state_counts"] = count_system_state()  # type: ignore

    return service_info


def generate_run_id() -> str:
    return str(uuid4())


def get_run_dir(run_id: str, run_base_dir: Optional[Path] = None) -> Path:
    if run_base_dir is None:
        run_base_dir = current_app.config["RUN_DIR"]

    return run_base_dir.joinpath(run_id[:2]).joinpath(run_id).resolve()


def get_path(run_id: str, file_type: str,
             run_base_dir: Optional[Path] = None) -> Path:
    run_dir: Path = get_run_dir(run_id, run_base_dir)

    return run_dir.joinpath(RUN_DIR_STRUCTURE[file_type])


def write_file(run_id: str, file_type: str, content: str,
               run_base_dir: Optional[Path] = None) -> None:
    file: Path = get_path(run_id, file_type, run_base_dir)
    file.parent.mkdir(parents=True, exist_ok=True)
    with file.open(mode="w") as f:
        f.write(content)


def flatten_wf_engine_params(wf_engine_params: str,
                             service_info_path: Optional[Path] = None) \
        -> List[str]:
    wf_engine_params_obj = json.loads(wf_engine_params)
    params: List[str] = read_default_wf_engine_params(service_info_path)
    for key, val in wf_engine_params_obj.items():
        params.append(key)
        if isinstance(val, list):
            params.append(",".join(val))
        else:
            try:
                params.append(str(val))
            except Exception:
                current_app.logger.debug(format_exc())

    return params


def get_all_run_ids() -> List[str]:
    run_base_dir: Path = current_app.config["RUN_DIR"]
    run_requests: List[Path] = \
        list(run_base_dir.glob(f"**/{RUN_DIR_STRUCTURE['run_request']}"))
    run_ids: List[str] = \
        [run_request.parent.name for run_request in run_requests]

    return run_ids


def get_state(run_id: str) -> State:
    try:
        with get_path(run_id, "state").open(mode="r") as f:
            str_state: str = \
                [line for line in f.read().splitlines() if line != ""][0]
        return State[str_state]
    except Exception:
        return State.UNKNOWN


def read_file(run_id: str, file_type: str) -> Any:
    file: Path = get_path(run_id, file_type)
    if file.exists() is False:
        if file_type in ["cmd", "start_time", "end_time", "stdout", "stderr",
                         "exit_code"]:
            return ""
        elif file_type == "task_logs":
            return []
        elif file_type in ["run_request", "outputs"]:
            return {}
        else:
            return ""
    with file.open(mode="r") as f:
        if file_type in ["cmd", "start_time", "end_time", "exit_code"]:
            return f.read().splitlines()[0]
        elif file_type in ["stdout", "stderr"]:
            return f.read()
        elif file_type in ["run_request", "outputs", "task_logs"]:
            return json.load(f)
        else:
            return f.read()


def get_outputs(run_id: str) -> Dict[str, str]:
    cmd: List[str] = shlex.split(read_file(run_id, "cmd"))
    outdir_ind: int = cmd.index("--outdir") + 1
    outdir_path: Path = Path(cmd[outdir_ind]).resolve()
    output_files: List[Path] = sorted(list(walk_all_files(outdir_path)))
    outputs: Dict[str, str] = {}
    for output_file in output_files:
        outputs[str(output_file.relative_to(outdir_path))] = \
            str(output_file)

    return outputs


def walk_all_files(dir: Path) -> Iterable[Path]:
    for root, dirs, files in os.walk(dir):
        for file in files:
            yield Path(root).joinpath(file)


def count_system_state() -> Dict[str, int]:
    run_ids: List[str] = get_all_run_ids()
    count: Dict[str, int] = \
        dict(collections.Counter(
            [get_state(run_id).name for run_id in run_ids]))

    return count


def read_default_wf_engine_params(service_info_path: Optional[Path] = None) \
        -> List[str]:
    default_wf_engine_params: List[DefaultWorkflowEngineParameter] = \
        read_service_info(service_info_path)[
            "default_workflow_engine_parameters"]
    params: List[str] = []
    for param in default_wf_engine_params:
        params.append(str(param.get("name", "")))
        params.append(str(param.get("default_value", "")))

    return params
