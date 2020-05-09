#!/usr/bin/env python3
# coding: utf-8
import argparse
import os
from argparse import ArgumentParser, Namespace
from pathlib import Path
from traceback import format_exc
from typing import List, Optional

from flask import Flask, Response, current_app, jsonify
from werkzeug.exceptions import HTTPException

from genpei.const import DEFAULT_HOST, DEFAULT_PORT, DEFAULT_RUN_DIR
from genpei.controller import app_bp
from genpei.type import ErrorResponse


def parse_args() -> Namespace:
    parser: ArgumentParser = argparse.ArgumentParser(
        description="An implementation of GA4GH Workflow Execution " +
                    "Service Standard as a microservice")

    parser.add_argument(
        "--host",
        nargs=1,
        type=str,
        metavar="",
        help=f"Host address of Flask. (default: {DEFAULT_HOST})"
    )
    parser.add_argument(
        "-p",
        "--port",
        nargs=1,
        type=int,
        metavar="",
        help=f"Port of Flask. (default: {DEFAULT_PORT})"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        metavar="",
        help="Enable debug mode of Flask."
    )
    parser.add_argument(
        "-r",
        "--run-dir",
        nargs=1,
        type=str,
        metavar="",
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


def fix_errorhandler(app: Flask) -> Flask:
    @app.errorhandler(400)
    @app.errorhandler(401)
    @app.errorhandler(403)
    @app.errorhandler(404)
    @app.errorhandler(500)
    def error_handler(error: HTTPException) -> Response:
        res_body: ErrorResponse = {
            "msg": error.description,  # type: ignore
            "status_code": error.code,  # type: ignore
        }
        response: Response = jsonify(res_body)
        response.status_code = error.code  # type: ignore
        return response

    @app.errorhandler(Exception)
    def error_handler_exception(exception: Exception) -> Response:
        current_app.logger.error(exception.args[0])
        current_app.logger.debug(format_exc())
        res_body: ErrorResponse = {
            "msg": "The server encountered an internal error and was " +
                   "unable to complete your request.",
            "status_code": 500,
        }
        response: Response = jsonify(res_body)
        response.status_code = 500
        return response

    return app


def create_app(run_dir: Path) -> Flask:
    app = Flask(__name__)
    app.register_blueprint(app_bp)
    fix_errorhandler(app)
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
