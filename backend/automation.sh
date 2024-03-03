#!/bin/bash

python3 -m pip install -r requirements.txt
pip3 install requests
pip3 install psycopg2-binary 
pip3 install djangorestframework
python3 manage.py makemigrations