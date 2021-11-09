import boto3
from botocore.config import Config

#Specify us-east-2 Ohio

def create_database(region, commands):
  try:
    database_region = Config(region_name=region)
    database_resource = boto3.resource("ec2", config=database_region)

    database_instance = database_resource.create_instances(
        ImageId="ami-020db2c14939a8efb",
        MinCount=1,
        MaxCount=1,
        InstanceType="t2.micro",
        KeyName="antonio.fuziy",
        UserData=commands
    )
    print("Database Created!")
    return database_instance
  except Exception as e:
    print(e)
    return False