import boto3
from botocore.config import Config

#Specify us-east-2 Ohio

def create_database(region, machine_id, security_group):
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
      UserData=run_postgres
    )
    print("")
    print("Creating Database Instance...")
    database_instance[0].wait_until_running()

    print("")
    print("Database Created!")
    return database_instance
  except Exception as e:
    print(e)
    return False