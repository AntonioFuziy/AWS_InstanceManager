import boto3
import os
from botocore.config import Config
from commands import run_postgres

database_region =  Config(region_name="us-east-1")
database_resource = boto3.resource("ec2", config=database_region)

database_instance = database_resource.create_instances(
    ImageId="ami-0279c3b3186e54acd",
    MinCount=1,
    MaxCount=1,
    InstanceType="t2.micro",
    UserData=run_postgres
)