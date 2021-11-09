import boto3
from botocore.config import Config

#Specify us-east-1 North Virginia

def create_django(region, commands):
  try:
    django_region = Config(region_name=region)
    django_resource = boto3.resource("ec2", config=django_region)

    django_instance = django_resource.create_instances(
        ImageId="ami-0279c3b3186e54acd",
        MinCount=1,
        MaxCount=1,
        InstanceType="t2.micro",
        KeyName="antonio.fuziy",
        UserData=commands
    )
    print("Djando Server Created!")
    return django_instance
  except Exception as e:
    print(e)
    return False