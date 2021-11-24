from utils import print_errors, print_successes, print_warnings, print_lines

def create_listener(ec2, target_group_arn, load_balancer_arn):
  try:
    print_lines("")
    print_lines("====================================")
    print_lines("Creating listener...")
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
  except Exception as e:
    print_lines("")
    print_errors("====================================")
    print_errors("Error creating listener")
    print_errors("====================================")
    print(e)

def delete_listeners(ec2, load_balancer_arn):
  try:
    print_lines("")
    print_lines("====================================")
    print_lines("Deleting listener...")
    all_listeners = ec2.describe_listeners(LoadBalancerArn=load_balancer_arn)
    if len(all_listeners["TargetGroups"]) > 0:
      for listener in all_listeners["Listeners"]:
        if listener["LoadBalancerArn"] == load_balancer_arn:
          ec2.delete_listener(ListenerArn=listener["ListenerArn"])
          print_successes("Listener deleted")
    else:
      print_warnings("No listeners available")
      return

  except Exception as e:
    print_lines("")
    print_errors("====================================")
    print_errors("Error deleting listener")
    print_errors("====================================")
    print(e)