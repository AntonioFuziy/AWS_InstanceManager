def get_subnets(ec2):
  subnets = ec2.describe_subnets()
  subnets_list = []
  for subnet in subnets["Subnets"]:
    subnets_list.append(subnet["SubnetId"])
  return subnets_list