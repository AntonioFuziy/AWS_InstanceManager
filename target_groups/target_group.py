
from utils import print_errors, print_successes, print_warnings, print_lines

def create_target_groups(ec2_north_virginia, ec2_load_balancer):
  try:
    target_groups = ec2_north_virginia.describe_vpcs()
    vpc_id = target_groups["Vpcs"][0]["VpcId"]

    print_lines("")
    print_lines("====================================")
    print_lines("Creating TARGET GROUP...")

    ec2_load_balancer.create_target_group(
      Name="instance-manager-target",
      Protocol="HTTP",
      Port=8080,
      TargetType="instance",
      VpcId=vpc_id
    )

    new_target_group = ec2_load_balancer.describe_target_groups(
      Names=["instance-manager-target"]
    )

    print_lines("")
    print_successes("====================================")
    print_successes("TARGET GROUP created")

    return new_target_group["TargetGroups"][0]["TargetGroupArn"]

  except Exception as e:
    print_lines("")
    print_errors("====================================")
    print_errors("ERROR:")
    print_errors("====================================")
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

    else:
      print_lines("")
      print_warnings("====================================")
      print_warnings("No Target Groups Available")
      return

  except Exception as e:
    print_lines("")
    print_errors("====================================")
    print_errors("ERROR:")
    print_errors("====================================")
    print(e)
    return False