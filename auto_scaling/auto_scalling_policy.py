from log import logging
from utils import print_successes, print_lines, print_warnings

def create_auto_scalling_policy(ec2, target_group_arn, load_balancer_arn):
  try: 
    print("")
    print_lines("Creating polocy...")
    logging.info("Creating policy...")
    load_balancer_name = load_balancer_arn[load_balancer_arn.find("app"):]
    target_group_name = target_group_arn[target_group_arn.find("targetgroup"):]
    
    ec2.put_scaling_policy(
      AutoScalingGroupName="auto_scaling_group",
      PolicyName="TargetTrackingScaling",
      PolicyType="TargetTrackingScaling",
      TargetTrackingConfiguration={
        "PredefinedMetricSpecification": {
          "PredefinedMetricType": "ALBRequestCountPerTarget",
          "ResourceLabel": f"{load_balancer_name}/{target_group_name}"
        },
        "TargetValue": 50
      }
    )

    print_successes("Policy created")
    logging.info("Policy created")
  except:
    print("")
    print_warnings("============================================")
    print_warnings("Could not create policy")
    print_warnings("============================================")
    logging.warning("Could not create policy")