import boto3
from botocore.config import Config
from utils import print_errors, print_successes, print_lines
from log import logging

def create_load_balancer_security_group(region):
    try:
        load_balancer_region = Config(region_name=region)
        load_balancer_resource = boto3.resource("ec2", config=load_balancer_region)

        security_group_load_balancer = load_balancer_resource.create_security_group(
            Description='allowing ports',
            GroupName='load_balancer_security_group',
            TagSpecifications=[
                {
                    'ResourceType': 'security-group',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': 'load_balancer'
                        },
                    ]
                },
            ],
        )
        print("")
        print_successes("====================================")
        print_successes("load balancer security-group created")
        logging.info("Load Balancer security-group created")
        
        security_group_load_balancer.authorize_ingress(
            CidrIp="0.0.0.0/0",
            FromPort=80,
            ToPort=80,
            IpProtocol="tcp"
        )
        logging.info("Load Balancer port 80 enabled")

        security_group_load_balancer.load()
        print_successes("LOAD BALANCER PORTS RUNNING")
        logging.info("Load Balancer ports running")

        return security_group_load_balancer
    except Exception as e:
        print("")
        print_errors("============================================")
        print_errors("MAYBE THIS SECURITY-GROUP IS ALREADY CREATED")
        print_errors("============================================")
        logging.error(e)
        print(e)
        return False