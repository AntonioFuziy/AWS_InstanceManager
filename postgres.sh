#!/bin/bash
cd /
sudo apt update && sudo apt install postgresql postgresql-contrib -y
sudo -i -u postgres bash << EOF
createuser -s cloud -W
createdb -O cloud tasks
echo "listen_addresses = '*'" >>  /etc/postgresql/12/main/postgresql.conf
echo "host all all 0.0.0.0/0 trust" >> /etc/postgresql/12/main/pg_hba.conf
EOF
sudo ufw allow 5432/tcp
sudo systemctl restart postgresql