#!/bin/bash
set -eux

URL="localhost:8080"

curl -X GET ${URL}/service-info
curl -X GET ${URL}/runs
curl -X GET ${URL}/runs/test_id
curl -X POST ${URL}/runs/test_id/cancel
curl -X GET ${URL}/runs/test_id/status
