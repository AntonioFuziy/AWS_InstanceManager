from utils import print_errors, print_successes, print_warnings, print_lines
from log import logging

def create_target_groups(ec2_north_virginia, ec2_load_balancer):
  try:
    target_groups = ec2_north_virginia.describe_vpcs()
    vpc_id = target_groups["Vpcs"][0]["VpcId"]

    print_lines("")
    print_lines("====================================")
    print_lines("Creating TARGET GROUP...")
    logging.info("Creating Target Group...")

    target_group_created = ec2_load_balancer.create_target_group(
      Name="instance-manager-target",
      Protocol="HTTP",
      Port=8080,
      HealthCheckEnabled=True,
      HealthCheckProtocol='HTTP',
      HealthCheckPort='8080',
      HealthCheckPath='/admin/',
      Matcher={
        'HttpCode': '200,302,301,404,403',
      },
      TargetType="instance",
      VpcId=vpc_id
    )

    # new_target_group = ec2_load_balancer.describe_target_groups(
    #   Names=["instance-manager-target"]
    # )

    new_target_group = target_group_created["TargetGroups"][0]["TargetGroupArn"]

    print_lines("")
    print_successes("====================================")
    print_successes("TARGET GROUP created")
    logging.info("Target-Group created")

    return new_target_group

  except Exception as e:
    print_lines("")
    print_errors("====================================")
    print_errors("ERROR:")
    print_errors("====================================")
    logging.error(e)
    print(e)
    return False

def delete_target_groups(ec2_load_balancer):
  try:
    target_groups = ec2_load_balancer.describe_target_groups()
    if len(target_groups["TargetGroups"]) > 0:
      for target_group in target_groups["TargetGroups"]:
        if target_group["TargetGroupName"] == "instance-manager-target":
          ec2_load_balancer.delete_target_group(TargetGroupArn=target_group["TargetGroupArn"])
          print_lines("")
          print_successes("====================================")
          print_successes("Target Group deleted")
          logging.info("Target-Group deleted")

    else:
      print_lines("")
      print_warnings("====================================")
      print_warnings("No Target Groups Available")
      logging.warning("No Target-Groups available")
      return

  except Exception as e:
    print_lines("")
    print_errors("====================================")
    print_errors("ERROR:")
    print_errors("====================================")
    logging.error(e)
    print(e)
    return False