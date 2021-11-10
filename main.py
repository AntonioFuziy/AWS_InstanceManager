import boto3
import os
from botocore.config import Config
from django import create_django
from postgres import create_database
from security_groups.django import create_django_security_group
from security_groups.postgres import create_database_security_group

#us-east-1
AMI_ID_NORTH_VIRGINIA_ID="ami-0279c3b3186e54acd"

#us-east-2
AMI_ID_OHIO_ID="ami-020db2c14939a8efb"

# creating database and its security-group
postgres_security_group = create_database_security_group("us-east-1")
postgres_instance = create_database("us-east-1", AMI_ID_NORTH_VIRGINIA_ID, postgres_security_group)
POSTGRES_IP = postgres_instance[0].public_ip_address

# creating django and its security-group
django_security_group = create_django_security_group("us-east-1")
django_instance = create_django("us-east-1", AMI_ID_NORTH_VIRGINIA_ID, POSTGRES_IP, django_security_group)