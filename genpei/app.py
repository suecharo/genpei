#!/usr/bin/env python3
# coding: utf-8
import argparse
import os
from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import List, Optional

from flask import Flask

from genpei.const import DEFAULT_HOST, DEFAULT_PORT, DEFAULT_RUN_DIR
from genpei.controller import app_bp


def parse_args() -> Namespace:
    parser: ArgumentParser = argparse.ArgumentParser(
        description="Implementation of GA4GH WES OpenAPI specification " +
                    "using cwltool.")

    parser.add_argument(
        "--host",
        nargs=1,
        type=str,
        help="Host address of Flask. (default: 127.0.0.1)"
    )
    parser.add_argument(
        "-p",
        "--port",
        nargs=1,
        type=int,
        help="Port of Flask. (default: 8080)"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode of Flask."
    )
    parser.add_argument(
        "-r",
        "--run-dir",
        nargs=1,
        type=str,
        help="Specify the run dir. (default: ./run)"
    )

    args: Namespace = parser.parse_args()

    return args


def handle_default_host(host: Optional[List[str]]) -> str:
    if host is None:
        return os.environ.get("GENPEI_HOST", DEFAULT_HOST)

    return host[0]


def handle_default_port(port: Optional[List[str]]) -> int:
    if port is None:
        return int(os.environ.get("GENPEI_PORT", DEFAULT_PORT))

    return int(port[0])


def handle_default_debug(debug: bool) -> bool:
    if debug is False:
        return bool(os.environ.get("GENPEI_DEBUG", False))

    return debug


def handle_default_run_dir(run_dir: Optional[List[str]]) -> Path:
    run_dir_path: Path
    if run_dir is None:
        run_dir_path = Path(os.environ.get("GENPEI_RUN_DIR", DEFAULT_RUN_DIR))
    else:
        run_dir_path = Path(run_dir[0])
    if not run_dir_path.is_absolute():
        run_dir_path = Path.cwd().joinpath(run_dir_path).resolve()

    return run_dir_path


def create_app(run_dir: Path) -> Flask:
    app = Flask(__name__)
    app.register_blueprint(app_bp)
    app.config["RUN_DIR"] = run_dir

    return app


def run(host: str, port: int, debug: bool, run_dir: Path) -> None:
    app: Flask = create_app(run_dir)
    app.run(host=host, port=port, debug=debug)


def main() -> None:
    args: Namespace = parse_args()
    host: str = handle_default_host(args.host)
    port: int = handle_default_port(args.port)
    debug: bool = handle_default_debug(args.debug)
    run_dir: Path = handle_default_run_dir(args.run_dir)

    run(host, port, debug, run_dir)


if __name__ == "__main__":
    main()
