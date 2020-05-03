#!/usr/bin/env python3
# coding: utf-8
from typing import Any, Dict, List

from flask import abort


def validate_run_request(run_request: Dict[Any, Any]) -> None:
    required_fields: List[str] = ["workflow_params",
                                  "workflow_type",
                                  "workflow_type_version",
                                  "workflow_url"]
    for field in required_fields:
        if field not in run_request:
            abort(400,
                  f"{field} not included in the form data of the request.")
