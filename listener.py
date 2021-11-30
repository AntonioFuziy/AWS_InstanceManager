from utils import print_errors, print_successes, print_warnings, print_lines
from log import logging

def create_listener(ec2, target_group_arn, load_balancer_arn):
  try:
    print_lines("")
    print_lines("====================================")
    print_lines("Creating listener...")
    logging.info("Creating listener...")
    ec2.create_listener(
      LoadBalancerArn=load_balancer_arn,
      Protocol='HTTP',
      Port=80,
      DefaultActions=[
        {
          'Type': 'forward',
          'TargetGroupArn': target_group_arn
        }
      ]
    )
    print_successes("Listener created")
    logging.info("Listener created")
  except Exception as e:
    print_lines("")
    print_errors("====================================")
    print_errors("Error creating listener")
    print_errors("====================================")
    logging.error(e)
    print(e)