#!/usr/bin/env python3
# coding: utf-8
from pathlib import Path
from typing import List

from setuptools import setup

BASE_DIR: Path = Path(__file__).parent.resolve()
REQUIREMNTS_TEXT: Path = BASE_DIR.joinpath("requirements.txt")


def read_requirements_txt() -> List[str]:
    with REQUIREMNTS_TEXT.open(mode="r") as f:
        packages: List[str] = \
            [str(line) for line in f.read().splitlines() if line != ""]

    return packages


def main() -> None:
    setup(name="stayhome_wes",
          version="1.0.0",
          description="Stayhome WES",
          author="suecharo",
          author_email="suehiro619@gmail.com",
          url="https://github.com/suecharo/stayhome_wes",
          license="Apache2.0",
          python_requires=">=3.6",
          platforms="any",
          include_package_data=True,
          zip_safe=False,
          classifiers=["Programming Language :: Python"],
          packages=["stayhome_wes"],
          install_requires=read_requirements_txt(),
          entry_points={
              "console_scripts": [
                  "stayhome_wes=stayhome_wes.app:main",
              ]
          }
          )


if __name__ == "__main__":
    main()
