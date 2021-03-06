#!/usr/bin/env python3
# coding: utf-8
import json
from pathlib import Path
from typing import BinaryIO, Dict, Tuple

import requests
from requests import Response

from genpei.type import RunRequest

URL: str = "localhost:8080"
SCRIPT_DIR: Path = \
    Path(__file__).parent.resolve()
RES_D: Path = \
    SCRIPT_DIR.parent.joinpath("resources").resolve()


def main() -> None:
    data: RunRequest = {
        "workflow_params": json.dumps({
            "fastq_1": {
                "class": "File",
                "location": str(RES_D.joinpath("ERR034597_1.small.fq.gz"))
            },
            "fastq_2": {
                "class": "File",
                "location": str(RES_D.joinpath("ERR034597_2.small.fq.gz"))
            }
        }),
        "workflow_type": "CWL",
        "workflow_type_version": "v1.0",
        "tags": json.dumps({
            "workflow_name": "trimming_and_qc"
        }),
        "workflow_engine_parameters": json.dumps({}),
        "workflow_url": str(RES_D.joinpath("trimming_and_qc.cwl"))
    }
    files: Dict[str, Tuple[str, BinaryIO]] = {}
    response: Response = requests.post(
        f"http://{URL}/runs", data=data, files=files)

    print(response.status_code)
    print(json.dumps(json.loads(response.text), indent=2))


if __name__ == "__main__":
    main()
