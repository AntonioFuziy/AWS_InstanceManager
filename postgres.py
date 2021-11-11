import boto3
from botocore.config import Config

#Specify us-east-2 Ohio

def create_database(region, machine_id, security_group):
  try:

    with open("django.sh", "r") as f:
      run_postgres = f.read()

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
    database_instance[0].reload()

    print("")
    print("Database Created!")
    return database_instance
  except Exception as e:
    print(e)
    return False