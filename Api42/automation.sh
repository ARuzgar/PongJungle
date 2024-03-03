#!/bin/bash

python3 -m pip install --upgrade pip
pip3 install virtualenv
python3 -m virtualenv .venv
source .venv/bin/activate
pip3 install serializers
pip3 install djangorestframework --upgrade