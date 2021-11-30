from utils import print_errors, print_successes, print_warnings, print_lines
from log import logging

def attach_load_balancer(ec2_auto_scalling, target_group_arn):
  try:
    print_lines("====================================")
    print_lines("Attaching load balancer to target group...")
    logging.info("Attaching load balancer to target group...")

    ec2_auto_scalling.attach_load_balancer_target_groups(
      AutoScalingGroupName='auto_scaling_group',
      TargetGroupARNs=[
        target_group_arn
      ]
    )
    print_lines("Load balancer attached successfully")
    logging.info("Load balancer attached successfully")
    return
  except Exception as e:
    print_lines("")
    print_errors("====================================")
    print_errors("ERROR")
    print_errors("====================================")
    logging.error(e)
    print(e)
    return False