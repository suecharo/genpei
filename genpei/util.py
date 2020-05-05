#!/usr/bin/env python3
# coding: utf-8
import json
from pathlib import Path
from typing import List
from uuid import uuid4

from cwltool.update import ALLUPDATES
from cwltool.utils import versionstring

from genpei.const import FILE_NAMES
from genpei.type import RunRequest, ServiceInfo

SRC_DIR: Path = Path(__file__).parent.resolve()
SERVICE_INFO_JSON: Path = \
    SRC_DIR.joinpath(FILE_NAMES["service_info"]).resolve()
RUN_DIR: Path = SRC_DIR.parent.joinpath("run").resolve()

CWLTOOL_VERSION: str = versionstring().strip().split(" ")[1]
CWL_VERSIONS: List[str] = list(map(str, ALLUPDATES.keys()))


def read_service_info() -> ServiceInfo:
    with SERVICE_INFO_JSON.open(mode="r") as f:
        service_info: ServiceInfo = json.load(f)
    service_info["workflow_engine_versions"]["cwltool"] = CWLTOOL_VERSION
    service_info["workflow_type_versions"]["CWL"]["workflow_type_version"] = \
        CWL_VERSIONS

    return service_info


def generate_run_id() -> str:
    return str(uuid4())


def get_run_dir(run_id: str) -> Path:
    return RUN_DIR.joinpath(run_id[:2]).joinpath(run_id).resolve()


def read_run_request(run_id: str) -> RunRequest:
    run_dir: Path = get_run_dir(run_id)
    with run_dir.joinpath(FILE_NAMES["run_request"]).open(mode="r") as f:
        run_request: RunRequest = json.load(f)

    return run_request
