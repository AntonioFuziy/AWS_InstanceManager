from subnets.subnets import get_subnets
from utils import print_errors, print_successes, print_warnings, print_lines
from log import logging

def create_loadbalancer(ec2_north_virginia, ec2_load_balancer, security_group, waiter):
  try:
    logging.info("Getting subnets")
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

    load_balancer_arn = load_balancer['LoadBalancers'][0]['LoadBalancerArn']

    # for balancer in load_balancer['LoadBalancers']:
    #   if balancer["LoadBalancerName"] == "load-balancer":
    #     load_balancer_arn = balancer["LoadBalancerArn"]

    print_lines("")
    print_lines("====================================")
    print_lines("Creating LOAD BALANCER...")
    logging.info("Creating LOAD BALANCER...")

    waiter.wait(LoadBalancerArns=[load_balancer_arn])
    print_successes("LOAD BALANCER Created!")
    logging.info("Load Balancer created")

    return load_balancer, load_balancer_arn
  except Exception as e:
    print_lines("")
    print_errors("====================================")
    print_errors("ERROR")
    print_errors("====================================")
    logging.error(e)
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
          logging.info("Deleting Load Balancer...")
          
          waiter.wait(LoadBalancerArns=[balancer["LoadBalancerArn"]])
          print_successes("LOAD BALANCER Deleted!")
          logging.info("Load Balancer deleted")
          # return balancer["LoadBalancerArn"]

    else:
      print_lines("")
      print_warnings("====================================")
      print_warnings("No LOAD BALANCERS available")
      logging.warning("No Load Balancer available")
      return
  except Exception as e:
    print_lines("")
    print_errors("====================================")
    print_errors("ERROR")
    print_errors("====================================")
    logging.error(e)
    print(e)
    return False