#!/usr/bin/env python3
# coding: utf-8
import json
from typing import BinaryIO, Dict, Tuple

import requests
from requests import Response

from genpei.type import RunRequest

URL = "localhost:8080"


def main() -> None:
    data: RunRequest = {
        "workflow_params": json.dumps({
            "key1": "value1",
            "key2": "value2",
        }),
        "workflow_type": "CWL",
        "workflow_type_version": "v1.0",
        "tags": json.dumps({
            "key1": "value1",
            "key2": "value2",
        }),
        "workflow_engine_parameters": json.dumps({
            "key1": "value1",
            "key2": "value2",
        }),
        "workflow_url": "test_workflow_url"
    }
    files: Dict[str, Tuple[str, BinaryIO]] = {
        "test1": ("test1.txt", open("./test1.txt", "rb")),
        "test2": ("test2.txt", open("./test2.txt", "rb")),
    }
    response: Response = \
        requests.post(f"http://{URL}/runs", data=data, files=files)

    print(response.status_code)
    print(response.content)


if __name__ == "__main__":
    main()
