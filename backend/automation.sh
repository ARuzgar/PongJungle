#!/bin/bash

python3 -m pip install --upgrade pip
pip3 install virtualenv
python3 -m virtualenv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
pip3 install requests
pip3 install psycopg2-binary 
pip3 install djangorestframework
python3 manage.py makemigrations