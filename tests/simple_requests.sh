#!/bin/bash
set -eux

URL="localhost:8080"

curl -X GET ${URL}/service-info
curl -X GET ${URL}/runs
