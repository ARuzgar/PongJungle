#!/bin/bash

python3 -m pip install --upgrade pip
pip3 install virtualenv
python3 -m virtualenv .venv
source .venv/bin/activate -y
python3 -m pip install -r requirements.txt
python3 manage.py makemigrations
pip3 install requests
pip3 install djangorestframework
python3 manage.py migrate
echo -e "\033[0;32mActivated virtual environments and starting the LocalHost..\033[0m"
python3 manage.py runserver 127.0.0.1:8000