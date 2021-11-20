import boto3

from ami.launch_image import delete_launch_ami
from auto_scaling.auto_scalling_group import delete_auto_scalling
from load_balancer.load_balancer import delete_loadbalancer
from target_groups.target_group import delete_target_groups
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

# deleting auto scalling
delete_auto_scalling(ec2_auto_scalling)

# deleting all load balancers
WAITER_DELETE_LOAD_BALANCER = ec2_load_balancer.get_waiter('load_balancers_deleted')
delete_loadbalancer(ec2_load_balancer, WAITER_DELETE_LOAD_BALANCER)

# deleting target groups
delete_target_groups(ec2_load_balancer)

# deleting launched image
delete_launch_ami(ec2_auto_scalling)

# deleting all images
delete_all_images(ec2_north_virginia_region, AMIS)

# deleting all instances
WAITER_NORTH_VIRIGINIA_INSTANCE = ec2_north_virginia_region.get_waiter('instance_terminated')
WAITER_OHIO_INSTANCE = ec2_ohio_region.get_waiter('instance_terminated')
delete_all_instances(ec2_north_virginia_region, WAITER_NORTH_VIRIGINIA_INSTANCE)
delete_all_instances(ec2_ohio_region, WAITER_OHIO_INSTANCE)

# deleting all security groups
delete_all_security_groups(ec2_north_virginia_region, SECURITY_GROUP_NAMES)
delete_all_security_groups(ec2_ohio_region, SECURITY_GROUP_NAMES)
delete_all_security_groups(ec2_north_virginia_region, SECURITY_GROUP_NAMES)