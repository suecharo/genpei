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
RESOURCE_DIR: Path = \
    SCRIPT_DIR.parent.joinpath("resources").resolve()
MOUNT_DIR: Path = \
    SCRIPT_DIR.parent.parent.joinpath("mount").resolve()


def main() -> None:
    data: RunRequest = {
        "workflow_params": json.dumps({
            "fastq_1": {
                "class": "File",
                "location": "./ERR034597_1.small.fq.gz"
            },
            "fastq_2": {
                "class": "File",
                "location": "./ERR034597_1.small.fq.gz"
            }
        }),
        "workflow_type": "CWL",
        "workflow_type_version": "v1.0",
        "tags": json.dumps({
            "workflow_name": "trimming_and_qc_remote"
        }),
        "workflow_engine_parameters": json.dumps({}),
        "workflow_url": "./trimming_and_qc.cwl"
    }
    files: Dict[str, Tuple[str, BinaryIO]] = {
        "fastq_1": ("ERR034597_1.small.fq.gz",
                    open(f"{RESOURCE_DIR}/ERR034597_1.small.fq.gz", "rb")),
        "fastq_2": ("ERR034597_2.small.fq.gz",
                    open(f"{RESOURCE_DIR}/ERR034597_2.small.fq.gz", "rb")),
        "workflow": ("trimming_and_qc.cwl",
                     open(f"{RESOURCE_DIR}/trimming_and_qc.cwl", "rb")),
        "tool_1": ("fastqc.cwl",
                   open(f"{RESOURCE_DIR}/fastqc.cwl", "rb")),
        "tool_2": ("trimmomatic_pe.cwl",
                   open(f"{RESOURCE_DIR}/trimmomatic_pe.cwl", "rb")),
    }
    response: Response = \
        requests.post(f"http://{URL}/runs", data=data, files=files)

    print(response.status_code)
    print(response.content)


if __name__ == "__main__":
    main()
