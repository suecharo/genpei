#!/usr/bin/env python3
# coding: utf-8
from flask import Flask

from genpei.controller import app_bp


def create_app() -> Flask:
    app = Flask(__name__)
    app.register_blueprint(app_bp)

    return app


def main() -> None:
    app: Flask = create_app()
    app.run(host="0.0.0.0", port=8080, debug=True)


if __name__ == "__main__":
    main()
