#!/bin/bash
SCRIPT_DIR=$(
    cd $(dirname $0)
    pwd
)
BASE_DIR=$(
    cd ${SCRIPT_DIR}/..
    pwd
)

isort $(find ${BASE_DIR} -name '*.py')
