import boto3
from botocore.config import Config

database_region =  Config(region_name="us-east-1")
database_resource = boto3.resource("ec2", config=database_region)

security_group_database = database_resource.create_security_group(
    Description='string',
    GroupName='database_security_group',
    TagSpecifications=[
        {
            'ResourceType': 'security-group',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'postgres'
                },
            ]
        },
    ],
)