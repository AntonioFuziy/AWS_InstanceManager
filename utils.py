def delete_all_instances(ec2, waiter):
  try:
    delete_instances_ids = []
    existing_instances = ec2.describe_instances()
    existing_instances = existing_instances["Reservations"]
    for instance in existing_instances:
      for i in instance["Instances"]:
        delete_instances_ids.append(i["InstanceId"])
    if len(delete_instances_ids) > 0:
      ec2.terminate_instances(InstanceIds=delete_instances_ids)
      print("")
      print("====================================================")
      print("Waiting for the delete process from all INSTANCES...")
      waiter.wait(InstanceIds=delete_instances_ids)
    else:
      print("")
      print("====================================")
      print("No instances to delete")
  except Exception as e:
    print("")
    print("====================================")
    print("ERROR")
    print("====================================")
    print(e)

def delete_all_security_groups(ec2, security_group_names):
  try:
    existing_security_groups = ec2.describe_security_groups()
    for security_group in existing_security_groups["SecurityGroups"]:
      if security_group["GroupName"] in security_group_names:
        print("")
        print("==========================================================")
        print("Waiting for the delete process from all SECURITY GROUPS...")
        ec2.delete_security_group(GroupId=security_group["GroupId"])
  except Exception as e:
    print("")
    print("====================================")
    print("ERROR")
    print("====================================")
    print(e)

def delete_all_images(ec2, AMIs):
  try:
    existing_images = ec2.describe_images(Owners=["self"])
    if len(existing_images["Images"]) > 0:
      for image in existing_images["Images"]:
        if image["Name"] in AMIs:
          print("")
          print("===============================================")
          print("Waiting for the delete process from all AMIs...")
          ec2.deregister_image(ImageId=image["ImageId"])
    else:
      print("")
      print("====================================")
      print("No AMIs existing")
      return
  except Exception as e:
    print("")
    print("====================================")
    print("ERROR")
    print("====================================")
    print(e)