import boto3
from botocore.config import Config
from utils import print_errors, print_successes, print_lines

def create_django_security_group(region):
    try:
        django_region = Config(region_name=region)
        django_resource = boto3.resource("ec2", config=django_region)

        security_group_django = django_resource.create_security_group(
            Description='allowing ports',
            GroupName='django_security_group',
            TagSpecifications=[
                {
                    'ResourceType': 'security-group',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': 'django'
                        },
                    ]
                },
            ],
        )
        print("")
        print_successes("====================================")
        print_successes("Django security-group created")

        security_group_django.authorize_ingress(
            CidrIp="0.0.0.0/0",
            FromPort=22,
            ToPort=22,
            IpProtocol="tcp"
        )
        
        security_group_django.authorize_ingress(
            CidrIp="0.0.0.0/0",
            FromPort=8080,
            ToPort=8080,
            IpProtocol="tcp"
        )

        security_group_django.load()
        print_successes("DJANGO PORTS RUNNING")

        return security_group_django
    except Exception as e:
        print("")
        print_errors("============================================")
        print_errors("MAYBE THIS SECURITY-GROUP IS ALREADY CREATED")
        print_errors("============================================")
        print(e)
        return False