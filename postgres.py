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
  - sudo apt install postgresql postgresql-contrib -y
  - sudo su - postgres
  - sudo -u postgres psql -c "CREATE USER cloud WITH PASSWORD 'cloud';"
  - sudo -u postgres psql -c "CREATE DATABASE tasks;"
  - sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE tasks TO cloud;"
  - sudo echo "listen_addresses = '*'" >> /etc/postgresql/10/main/postgresql.conf
  - sudo echo "host all all 0.0.0.0/0 trust" >> /etc/postgresql/10/main/pg_hba.conf
  - sudo ufw allow 5432/tcp -y
  - sudo systemctl restart postgresql
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