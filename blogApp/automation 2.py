import os
import sys

os.system('pip3 install virtualenv')
os.system('virtualenv .venv')
os.system('source .venv/bin/activate')
os.system('python3 -m pip install -r requirements.txt')
os.system('python3 manage.py makemigrations')
os.system('python3 manage.py migrate')
os.system('python3 manage.py runserver 127.0.0.1:8000')
