#!/usr/bin/env python3
# coding: utf-8
import json
from pathlib import Path
from typing import List

from cwltool.update import ALLUPDATES
from cwltool.utils import versionstring

from stayhome_wes.type import ServiceInfo

SRC_DIR = Path(__file__).parent.resolve()
SERVICE_INFO_JSON: Path = SRC_DIR.joinpath("service-info.json").resolve()

CWLTOOL_VERSION: str = versionstring().strip()
CWL_VERSIONS: List[str] = list(map(str, ALLUPDATES.keys()))


def read_service_info() -> ServiceInfo:
    with SERVICE_INFO_JSON.open(mode="r") as f:
        service_info: ServiceInfo = json.load(f)

    return service_info
