#!/bin/sh

set -e

export PYTHONPATH=/opt/venv/lib/python3.10/site-packages:/usr/lib/python3/dist-packages
python3 echo-plus.py
