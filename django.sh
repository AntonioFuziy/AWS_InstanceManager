#!/bin/bash
sudo apt update
git clone https://github.com/raulikeda/tasks.git
cd tasks
sudo sed -i 's/node1/postgres_ip/g' ./portfolio/settings.py
./install.sh
sudo reboot