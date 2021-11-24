import boto3
from botocore.config import Config

from utils import print_errors, print_successes, print_lines

#Specify us-east-2 Ohio

def create_database(region, machine_id, security_group):
  postgres_script="""
  #cloud-config

  runcmd:
  - cd /
  - sudo apt update
  - echo "APT UPDATE" >> log.txt
  - sudo apt install postgresql postgresql-contrib -y
  - echo "INSTALL POSTGRES" >> log.txt
  - sudo su - postgres
  - echo "SUDO SU POSTGRES" >> log.txt
  - sudo -u postgres psql -c "CREATE USER cloud WITH PASSWORD 'cloud';"
  - echo "CREATE USER cloud" >> log.txt
  - sudo -u postgres psql -c "CREATE DATABASE tasks;"
  - echo "CREATE DATABASE tasks" >> log.txt
  - sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE tasks TO cloud;"
  - echo "PRIVILEGES" >> log.txt
  - sudo echo "listen_addresses = '*'" >> /etc/postgresql/10/main/postgresql.conf
  - echo "ENABLING ALL LISTENERS *" >> log.txt
  - sudo echo "host all all 0.0.0.0/0 trust" >> /etc/postgresql/10/main/pg_hba.conf
  - echo "TRUST ALL" >> log.txt
  - sudo ufw allow 5432/tcp -y
  - echo "UFW 5432" >> log.txt
  - sudo systemctl restart postgresql
  - echo "RESTARTING POSTGRES" >> log.txt
  """
  try:
    database_region = Config(region_name=region)
    database_resource = boto3.resource("ec2", config=database_region)

    database_instance = database_resource.create_instances(
      ImageId=machine_id,
      MinCount=1,
      MaxCount=1,
      InstanceType="t2.micro",
      KeyName="antonio.fuziy",
      SecurityGroupIds=[
        security_group.group_id
      ],
      TagSpecifications=[
        {
          "ResourceType": "instance",
          "Tags": [
            {
              "Key": "Name",
              "Value": "postgres"
            }
          ]
        }
      ],
      UserData=postgres_script
    )
    print_lines("")
    print_lines("====================================")
    print_lines("Creating Database Instance...")
    database_instance[0].wait_until_running()
    database_instance[0].reload()
    print_successes("Database Created!")

    return database_instance, database_instance[0].public_ip_address
  except Exception as e:
    print_lines("")
    print_errors("====================================")
    print_errors("ERROR")
    print_errors("====================================")
    print(e)
    return False