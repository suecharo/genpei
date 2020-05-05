#!/bin/bash
python3 /app/setup.py develop --uninstall
cp /app/MANIFEST.in ./
cp /app/requirements.txt ./
cp /app/setup.py ./
python3 ./setup.py develop

tail -f /dev/null
