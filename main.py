import boto3

from django import create_django
from ami.django_ami import create_django_AMI
from ami.launch_image import delete_launch_ami, launch_ami
from auto_scaling.auto_scalling_group import create_auto_scalling, delete_auto_scalling
from load_balancer.load_balancer import create_loadbalancer, delete_loadbalancer
from postgres import create_database
from listener import create_listener
from load_balancer.attach_load_balancer import attach_load_balancer
from security_groups.django import create_django_security_group
from security_groups.load_balancer import create_load_balancer_security_group
from security_groups.postgres import create_database_security_group
from target_groups.target_group import create_target_groups, delete_target_groups
from utils import delete_all_images, delete_all_instances, delete_all_security_groups

# AWS regions
NORTH_VIRGINIA_REGION = "us-east-1"
OHIO_REGION = "us-east-2"

# ubuntu 18.04 us-east-1 e us-east-2
AMI_ID_NORTH_VIRGINIA_ID="ami-0279c3b3186e54acd"
AMI_ID_OHIO_ID="ami-020db2c14939a8efb"

# name from all security-groups name
SECURITY_GROUP_NAMES = ["django_security_group", "database_security_group", "load_balancer_security_group"]

# name from all images name
AMIS = ["django_AMI"]

# getting ec2 client
ec2_ohio_region = boto3.client('ec2', region_name=OHIO_REGION)
ec2_north_virginia_region = boto3.client('ec2', region_name=NORTH_VIRGINIA_REGION)
ec2_load_balancer = boto3.client('elbv2', region_name=NORTH_VIRGINIA_REGION)
ec2_auto_scalling = boto3.client('autoscaling', region_name=NORTH_VIRGINIA_REGION)

# deleting all load balancers
WAITER_CREATE_LOAD_BALANCER = ec2_load_balancer.get_waiter('load_balancer_available')
WAITER_DELETE_LOAD_BALANCER = ec2_load_balancer.get_waiter('load_balancers_deleted')
delete_loadbalancer(ec2_load_balancer, WAITER_DELETE_LOAD_BALANCER)

# deleting auto scalling
delete_auto_scalling(ec2_auto_scalling)

# deleting launched image
delete_launch_ami(ec2_auto_scalling)

# deleting all images
WAITER_AMI = ec2_north_virginia_region.get_waiter('image_available')
delete_all_images(
  ec2_north_virginia_region, 
  AMIS
)

# deleting all instances
WAITER_NORTH_VIRGINIA_INSTANCE = ec2_north_virginia_region.get_waiter('instance_terminated')
WAITER_OHIO_INSTANCE = ec2_ohio_region.get_waiter('instance_terminated')
delete_all_instances(
  ec2_north_virginia_region, 
  WAITER_NORTH_VIRGINIA_INSTANCE
)
delete_all_instances(
  ec2_ohio_region, 
  WAITER_OHIO_INSTANCE
)

# deleting target groups
delete_target_groups(ec2_load_balancer)

# deleting all security-groups
delete_all_security_groups(
  ec2_north_virginia_region, 
  SECURITY_GROUP_NAMES
)
delete_all_security_groups(
  ec2_ohio_region, 
  SECURITY_GROUP_NAMES
)
delete_all_security_groups(
  ec2_north_virginia_region, 
  SECURITY_GROUP_NAMES
)

# creating database and its security-group
POSTGRES_SECURITY_GROUP = create_database_security_group(OHIO_REGION)
postgres_instance, POSTGRES_IP = create_database(
  OHIO_REGION, 
  AMI_ID_OHIO_ID, 
  POSTGRES_SECURITY_GROUP
)
if POSTGRES_IP:
  print(f"POSTGRES_IP: {POSTGRES_IP}")

# creating django and its security-group
DJANGO_SECURITY_GROUP = create_django_security_group(NORTH_VIRGINIA_REGION)
django_instance, DJANGO_ID, DJANGO_IP = create_django(
  NORTH_VIRGINIA_REGION, 
  AMI_ID_NORTH_VIRGINIA_ID, 
  POSTGRES_IP, 
  DJANGO_SECURITY_GROUP, 
  ec2_north_virginia_region
)
if DJANGO_IP:
  print(f"DJANGO_IP: {DJANGO_IP}")

# creating django AMI (IMAGE)
django_AMI, DJANGO_AMI_ID = create_django_AMI(
  ec2_north_virginia_region, 
  DJANGO_ID, 
  WAITER_AMI
)
if DJANGO_AMI_ID:
  print(f"DJANGO_AMI_ID: {DJANGO_AMI_ID}")

# delete django instance after AMI creation
delete_all_instances(
  ec2_north_virginia_region, 
  WAITER_NORTH_VIRGINIA_INSTANCE
)

# creating target group
TARGET_GROUP_ARN = create_target_groups(
  ec2_north_virginia_region, 
  ec2_load_balancer
) 

# creating load_balancer
LOAD_BALANCER_SECURITY_GROUP = create_load_balancer_security_group(NORTH_VIRGINIA_REGION)
load_balancer, load_balancer_arn = create_loadbalancer(
  ec2_north_virginia_region, 
  ec2_load_balancer, 
  LOAD_BALANCER_SECURITY_GROUP, 
  WAITER_CREATE_LOAD_BALANCER
)

# lauching AMI
launch_ami(
  ec2_auto_scalling, 
  DJANGO_AMI_ID, 
  DJANGO_SECURITY_GROUP
)

# creating auto scalling
create_auto_scalling(
  ec2_auto_scalling, 
  ec2_north_virginia_region, 
  TARGET_GROUP_ARN
)

# attaching load balancer to target group
attach_load_balancer(ec2_auto_scalling, TARGET_GROUP_ARN)

# creating listener
create_listener(
  ec2_load_balancer, 
  TARGET_GROUP_ARN, 
  load_balancer_arn
)