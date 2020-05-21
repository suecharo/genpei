#!/usr/bin/env python3
# coding: utf-8
from pathlib import Path
from typing import List

from setuptools import setup

BASE_DIR: Path = Path(__file__).parent.resolve()
REQUIREMENTS_TEXT: Path = BASE_DIR.joinpath("requirements.txt")
LONG_DESCRIPTION: Path = BASE_DIR.joinpath("README.md")


def read_requirements_txt() -> List[str]:
    with REQUIREMENTS_TEXT.open(mode="r") as f:
        packages: List[str] = \
            [str(line) for line in f.read().splitlines() if line != ""]

    return packages


def main() -> None:
    setup(name="genpei",
          version="1.0.2",
          description="An implementation of GA4GH Workflow Execution " +
                      "Service Standard as a microservice",
          long_description=LONG_DESCRIPTION.open(mode="r").read(),
          long_description_content_type="text/markdown",
          author="suecharo",
          author_email="suehiro619@gmail.com",
          url="https://github.com/suecharo/genpei",
          license="Apache2.0",
          python_requires=">=3.6",
          platforms="any",
          include_package_data=True,
          zip_safe=False,
          classifiers=["Programming Language :: Python"],
          packages=["genpei"],
          install_requires=read_requirements_txt(),
          entry_points={
              "console_scripts": [
                  "genpei=genpei.app:main",
              ]
          }
          )


if __name__ == "__main__":
    main()
