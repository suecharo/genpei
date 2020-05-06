#!/usr/bin/env python3
# coding: utf-8
import collections
import json
import os
import shlex
from pathlib import Path
from typing import Dict, Iterable, List
from uuid import uuid4

from cwltool.update import ALLUPDATES
from cwltool.utils import versionstring

from genpei.const import RUN_DIR_STRUCTURE
from genpei.type import RunRequest, ServiceInfo, State

SRC_DIR: Path = Path(__file__).parent.resolve()
SERVICE_INFO_JSON: Path = \
    SRC_DIR.joinpath(RUN_DIR_STRUCTURE["service_info"]).resolve()
RUN_DIR: Path = SRC_DIR.parent.joinpath("run").resolve()

CWLTOOL_VERSION: str = versionstring().strip()
CWL_VERSIONS: List[str] = list(map(str, ALLUPDATES.keys()))


def read_service_info() -> ServiceInfo:
    with SERVICE_INFO_JSON.open(mode="r") as f:
        service_info: ServiceInfo = json.load(f)
    service_info["workflow_engine_versions"]["cwltool"] = CWLTOOL_VERSION
    service_info["workflow_type_versions"]["CWL"]["workflow_type_version"] = \
        CWL_VERSIONS
    service_info["system_state_counts"] = count_state()  # type: ignore

    return service_info


def generate_run_id() -> str:
    return str(uuid4())


def get_run_dir(run_id: str) -> Path:
    return RUN_DIR.joinpath(run_id[:2]).joinpath(run_id).resolve()


def get_path(run_id: str, file_type: str) -> Path:
    return get_run_dir(run_id).joinpath(RUN_DIR_STRUCTURE[file_type])


def read_run_request(run_id: str) -> RunRequest:
    with get_path(run_id, "run_request").open(mode="r") as f:
        run_request: RunRequest = json.load(f)

    return run_request


def write_file(run_id: str, file_type: str, content: str) -> None:
    file: Path = get_path(run_id, file_type)
    file.parent.mkdir(parents=True, exist_ok=True)
    with file.open(mode="w") as f:
        f.write(content)


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


def get_all_run_ids() -> List[str]:
    run_requests: List[Path] = \
        list(RUN_DIR.glob(f"**/{RUN_DIR_STRUCTURE['run_request']}"))
    run_ids: List[str] = \
        [run_request.parent.name for run_request in run_requests]

    return run_ids


def get_state(run_id: str) -> State:
    try:
        state_file: Path = get_path(run_id, "state")
        with state_file.open(mode="r") as f:
            str_state: str = \
                [line for line in f.read().splitlines() if line != ""][0]
        state: State = State[str_state]
        return state
    except Exception:
        return State.UNKNOWN


def read_file(run_id: str, file_type: str) -> str:
    try:
        file: Path = get_path(run_id, file_type)
        with file.open(mode="r") as f:
            return f.read()
    except Exception:
        return ""  # TODO Error Handling


def read_cmd(run_id: str) -> List[str]:
    try:
        cmd_file: Path = get_path(run_id, "cmd")
        with cmd_file.open(mode="r") as f:
            cmd: str = \
                [line for line in f.read().splitlines() if line != ""][0]
            l_cmd: List[str] = shlex.split(cmd)
            return l_cmd
    except Exception:
        return []  # TODO Error Handling


def get_outputs(run_id: str) -> Dict[str, str]:
    try:
        cmd: List[str] = read_cmd(run_id)
        outdir_ind: int = cmd.index("--outdir") + 1
        outdir_path: Path = Path(cmd[outdir_ind])
        if not outdir_path.is_absolute():
            outdir_path = \
                get_path(run_id, "exe").joinpath(outdir_path).resolve()
        output_files: List[Path] = sorted(list(walk_all_files(outdir_path)))
        outputs: Dict[str, str] = {}
        for output_file in output_files:
            outputs[output_file.name] = str(output_file)
        return outputs
    except Exception:
        return {}  # TODO Error Handling


def walk_all_files(dir: Path) -> Iterable[Path]:
    for root, dirs, files in os.walk(dir):
        yield Path(root)
        for file in files:
            yield Path(root).joinpath(file)


def count_state() -> Dict[str, int]:
    run_ids: List[str] = get_all_run_ids()
    count: Dict[str, int] = \
        dict(collections.Counter(
            [get_state(run_id).name for run_id in run_ids]))

    return count
