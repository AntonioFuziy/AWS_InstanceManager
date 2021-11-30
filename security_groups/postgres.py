import boto3
from botocore.config import Config
from utils import print_errors, print_successes, print_lines
from log import logging

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
        print_successes("====================================")
        print_successes("Postgres security-group created")
        logging.info("Postgres security-group created")

        security_group_database.authorize_ingress(
            CidrIp="0.0.0.0/0",
            FromPort=22,
            ToPort=22,
            IpProtocol="tcp"
        )
        logging.info("Postgres port 22 enabled")
        
        security_group_database.authorize_ingress(
            CidrIp="0.0.0.0/0",
            FromPort=5432,
            ToPort=5432,
            IpProtocol="tcp"
        )
        logging.info("Postgres port 5432 enabled")

        security_group_database.load()
        print_successes("POSTGRES PORTS RUNNING")
        logging.info("Postgres ports running")

        return security_group_database
    except Exception as e:
        print("")
        print_errors("============================================")
        print_errors("MAYBE THIS SECURITY-GROUP IS ALREADY CREATED")
        print_errors("============================================")
        logging.error(e)
        print(e)
        return False