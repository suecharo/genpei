#!/usr/bin/env python3
# coding: utf-8
import json

import requests
from requests import Response

from stayhome_wes.type import RunRequest

URL = "localhost:8080"


def main():
    data: RunRequest = {
        "workflow_params": json.dumps({
            "key1": "value1",
            "key2": "value2",
        }),
        "workflow_type": "1",
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
    response: Response = requests.post(f"http://{URL}/runs", data=data)

    print(response.status_code)
    print(response.content)


if __name__ == "__main__":
    main()
