import boto3
from botocore.config import Config

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
        print("====================================")
        print("load balancer security-group created")
        
        security_group_load_balancer.authorize_ingress(
            CidrIp="0.0.0.0/0",
            FromPort=80,
            ToPort=80,
            IpProtocol="tcp"
        )

        security_group_load_balancer.load()
        print("LOAD BALANCER PORTS RUNNING")

        return security_group_load_balancer
    except Exception as e:
        print("")
        print("============================================")
        print("MAYBE THIS SECURITY-GROUP IS ALREADY CREATED")
        print("============================================")
        print(e)
        return False