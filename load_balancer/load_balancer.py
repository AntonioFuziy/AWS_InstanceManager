from subnets.subnets import get_subnets
from utils import print_errors, print_successes, print_warnings, print_lines

def create_loadbalancer(ec2_north_virginia, ec2_load_balancer, security_group, waiter):
  try:
    subnets = get_subnets(ec2_north_virginia)
    load_balancer = ec2_load_balancer.create_load_balancer(
      SecurityGroups=[
        security_group.group_id
      ],
      Tags=[
        {
          'Key': 'Name',
          'Value': 'load-balancer'
        }
      ],
      IpAddressType='ipv4',
      Name='load-balancer',
      Subnets=subnets
    )

    for balancer in load_balancer['LoadBalancers']:
      if balancer["LoadBalancerName"] == "load-balancer":
        load_balancer_arn = balancer["LoadBalancerArn"]

    print_lines("")
    print_lines("====================================")
    print_lines("Creating LOAD BALANCER...")

    waiter.wait(LoadBalancerArns=[load_balancer_arn])
    print_successes("LOAD BALANCER Created!")

    return load_balancer, load_balancer_arn
  except Exception as e:
    print_lines("")
    print_errors("====================================")
    print_errors("ERROR")
    print_errors("====================================")
    print(e)
    return False

def delete_loadbalancer(ec2_load_balancer, waiter):
  try:
    load_balancer = ec2_load_balancer.describe_load_balancers()
    if len(load_balancer['LoadBalancers']) > 0:
      for balancer in load_balancer['LoadBalancers']:
        if balancer["LoadBalancerName"] == "load-balancer":
          ec2_load_balancer.delete_load_balancer(LoadBalancerArn=balancer["LoadBalancerArn"])
          print_lines("")
          print_lines("====================================")
          print_lines("Deleting LOAD BALANCER...")
          
          waiter.wait(LoadBalancerArns=[balancer["LoadBalancerArn"]])
          print_successes("LOAD BALANCER Deleted!")
          # return balancer["LoadBalancerArn"]

    else:
      print_lines("")
      print_warnings("====================================")
      print_warnings("No LOAD BALANCERS available")
      return
  except Exception as e:
    print_lines("")
    print_errors("====================================")
    print_errors("ERROR")
    print_errors("====================================")
    print(e)
    return False