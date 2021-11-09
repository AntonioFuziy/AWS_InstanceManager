import boto3
import os
from botocore.config import Config
from django import create_django
from postgres import create_database

run_postgres = '''
#!/bin/bash
sudo apt update
sudo apt install postgresql postgresql-contrib -y
sudo -i -u postgres bash << EOF
createuser -s cloud -W
cloud
createdb -O cloud tasks
echo "listen_addresses = '*'" >>  /etc/postgresql/12/main/postgresql.conf
echo "host all all 0.0.0.0/0 trust" >> /etc/postgresql/12/main/pg_hba.conf
EOF
sudo ufw allow 5432/tcp
sudo systemctl restart postgresql
'''

run_django='''
#!/bin/bash
sudo apt update
git clone https://github.com/raulikeda/tasks.git
cd tasks
sudo sed -i 's/node1/{public_ip_postgres}/g' portfolio/settings.py
./install.sh
sudo reboot
'''

postgres_instance = create_database("us-east-2", run_postgres)
# django_instance = create_django("us-east-1", run_django)