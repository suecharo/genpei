#!/usr/bin/env python3
# coding: utf-8
import json

import requests
from requests import Response

from genpei.util import get_all_run_ids

URL: str = "localhost:8080"


def main() -> None:
    run_id: str = get_all_run_ids()[0]
    response: Response = \
        requests.get(f"http://{URL}/runs/{run_id}/status")

    print(response.status_code)
    print(json.dumps(json.loads(response.text), indent=2))


if __name__ == "__main__":
    main()
