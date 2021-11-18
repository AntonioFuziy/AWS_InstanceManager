import boto3
import os
from botocore.config import Config

from django import create_django
from ami.django_ami import create_django_AMI
from postgres import create_database
from security_groups.django import create_django_security_group
from security_groups.postgres import create_database_security_group
from utils import delete_all_images, delete_all_instances, delete_all_security_groups

# AWS regions
NORTH_VIRGINIA_REGION = "us-east-1"
OHIO_REGION = "us-east-2"

# ubuntu 18.04 us-east-1 e us-east-2
AMI_ID_NORTH_VIRGINIA_ID="ami-0279c3b3186e54acd"
AMI_ID_OHIO_ID="ami-020db2c14939a8efb"

#name from all security-groups name
security_group_names = ["django_security_group", "database_security_group"]

#name from all images name
AMIs = ["django_image"]

# getting ec2 client
ec2_ohio_region = boto3.client('ec2', region_name=OHIO_REGION)
ec2_north_virginia_region = boto3.client('ec2', region_name=NORTH_VIRGINIA_REGION)

#deleting all images
waiter_ami = ec2_north_virginia_region.get_waiter('image_available')
delete_all_images(ec2_north_virginia_region, AMIs)

# deleting all instances
waiter_north_virginia = ec2_north_virginia_region.get_waiter('instance_terminated')
waiter_ohio = ec2_ohio_region.get_waiter('instance_terminated')
delete_all_instances(ec2_north_virginia_region, waiter_north_virginia)
delete_all_instances(ec2_ohio_region, waiter_ohio)

# deleting all security-groups
delete_all_security_groups(ec2_north_virginia_region, security_group_names)
delete_all_security_groups(ec2_ohio_region, security_group_names)

# creating database and its security-group
postgres_security_group = create_database_security_group(OHIO_REGION)
postgres_instance, POSTGRES_IP = create_database(OHIO_REGION, AMI_ID_OHIO_ID, postgres_security_group)
if POSTGRES_IP:
  print(f"POSTGRES_IP: {POSTGRES_IP}")

# creating django and its security-group
django_security_group = create_django_security_group(NORTH_VIRGINIA_REGION)
django_instance, DJANGO_ID, DJANGO_IP = create_django(NORTH_VIRGINIA_REGION, AMI_ID_NORTH_VIRGINIA_ID, POSTGRES_IP, django_security_group, ec2_north_virginia_region)
if DJANGO_IP:
  print(f"DJANGO_IP: {DJANGO_IP}")

# creating django AMI (IMAGE)
django_AMI, DJANGO_AMI_ID = create_django_AMI(ec2_north_virginia_region, DJANGO_ID, waiter_ami)
if DJANGO_AMI_ID:
  print(f"DJANGO_AMI_ID: {DJANGO_AMI_ID}")