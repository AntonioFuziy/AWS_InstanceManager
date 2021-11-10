import boto3
from botocore.config import Config

def create_database_security_group(region):
    try:
        database_region = Config(region_name=region)
        database_resource = boto3.resource("ec2", config=database_region)

        security_group_database = database_resource.create_security_group(
            Description='allowing ports',
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
        print("")
        print("Postgres security-group created")

        security_group_database.authorize_ingress(
            CidrIp="0.0.0.0/0",
            FromPort=22,
            ToPort=22,
            IpProtocol="tcp"
        )
        
        security_group_database.authorize_ingress(
            CidrIp="0.0.0.0/0",
            FromPort=5432,
            ToPort=5432,
            IpProtocol="tcp"
        )

        security_group_database.load()

        print("")
        print("PORTS RUNNING")

        return security_group_database
    except Exception as e:
        print(e)
        print("")
        print("MAYBE THIS SECURITY-GROUP IS ALREADY CREATED")
        return False