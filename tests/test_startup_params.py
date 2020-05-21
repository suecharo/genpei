#!/usr/bin/env python3
# coding: utf-8
from argparse import Namespace
from pathlib import Path
from typing import Dict, Union

from _pytest.monkeypatch import MonkeyPatch
from flask import Flask

from genpei.app import create_app, handle_default_params, parse_args
from genpei.const import DEFAULT_HOST, DEFAULT_PORT

base_dir: Path = Path(__file__).parent.parent.resolve()


def test_default_params(delete_env_vars: None) -> None:
    args: Namespace = parse_args([])
    params: Dict[str, Union[str, int, Path]] = handle_default_params(args)
    app: Flask = create_app(params)

    assert params["host"] == DEFAULT_HOST
    assert params["port"] == DEFAULT_PORT
    assert params["debug"] is False
    assert app.config["RUN_DIR"] == base_dir.joinpath("run")
    assert app.config["SERVICE_INFO"] == \
        base_dir.joinpath("genpei/service-info.json")


def test_env_vars(delete_env_vars: None, monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setenv("GENPEI_HOST", "127.0.0.1")
    monkeypatch.setenv("GENPEI_PORT", "8888")
    monkeypatch.setenv("GENPEI_DEBUG", "True")
    monkeypatch.setenv("GENPEI_RUN_DIR", str(base_dir.joinpath("run")))
    monkeypatch.setenv("GENPEI_SERVICE_INFO",
                       str(base_dir.joinpath("genpei/service-info.json")))

    args: Namespace = parse_args([])
    params: Dict[str, Union[str, int, Path]] = handle_default_params(args)
    app: Flask = create_app(params)

    assert params["host"] == "127.0.0.1"
    assert params["port"] == 8888
    assert params["debug"] is True
    assert app.config["RUN_DIR"] == base_dir.joinpath("run")
    assert app.config["SERVICE_INFO"] == \
        base_dir.joinpath("genpei/service-info.json")


def test_parse_args(delete_env_vars: None) -> None:
    args: Namespace = \
        parse_args(["--host", "127.0.0.1",
                    "--port", "8888",
                    "--debug",
                    "--run-dir", str(base_dir.joinpath("run")),
                    "--service-info",
                    str(base_dir.joinpath("genpei/service-info.json"))])
    params: Dict[str, Union[str, int, Path]] = handle_default_params(args)
    app: Flask = create_app(params)

    assert params["host"] == "127.0.0.1"
    assert params["port"] == 8888
    assert params["debug"] is True
    assert app.config["RUN_DIR"] == base_dir.joinpath("run")
    assert app.config["SERVICE_INFO"] == \
        base_dir.joinpath("genpei/service-info.json")
