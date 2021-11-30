from log import logging
from colorama import Fore

def print_successes(text):
  print(Fore.GREEN + text)
  return

def print_warnings(text):
  print(Fore.YELLOW + text)
  return

def print_errors(text):
  print(Fore.RED + text)
  return

def print_lines(text):
  print(Fore.WHITE + text)
  return

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
      print_lines("")
      print_lines("====================================================")
      print_lines("Waiting for the delete process from all INSTANCES...")
      logging.info("Deleting instance...")
      waiter.wait(InstanceIds=delete_instances_ids)
      print_successes("Instance deleted")
      logging.info("Instance deleted")
    else:
      print_lines("")
      print_warnings("====================================")
      print_warnings("No instances to delete")
      logging.warning("No instances to delete")
      return
  except Exception as e:
    print_lines("")
    print_errors("====================================")
    print_errors("ERROR")
    print_errors("====================================")
    logging.error(e)
    print(e)

def delete_all_security_groups(ec2, security_group_names):
  try:
    existing_security_groups = ec2.describe_security_groups()
    for security_group in existing_security_groups["SecurityGroups"]:
      if security_group["GroupName"] in security_group_names:
        print_lines("")
        print_lines("==========================================================")
        print_lines("Waiting for the delete process from all SECURITY GROUPS...")
        logging.info("Deleting security-group...")
        ec2.delete_security_group(GroupId=security_group["GroupId"])
        print_successes("Security Group deleted")
        logging.info("Security-Group deleted")
  except Exception as e:
    print_lines("")
    print_errors("====================================")
    print_errors("ERROR")
    print_errors("====================================")
    logging.error(e)
    print(e)

def delete_all_images(ec2, AMIs):
  try:
    existing_images = ec2.describe_images(Owners=["self"])
    if len(existing_images["Images"]) > 0:
      for image in existing_images["Images"]:
        if image["Name"] in AMIs:
          print_lines("")
          print_lines("===============================================")
          print_lines("Waiting for the delete process from all AMIs...")
          logging.info("Deleting AMI...")
          ec2.deregister_image(ImageId=image["ImageId"])
          print_successes("AMIs deleted")
          logging.info("AMI deleted")
    else:
      print_lines("")
      print_warnings("====================================")
      print_warnings("No AMIs existing")
      logging.warning("No AMIs to delete")
      return
  except Exception as e:
    print_lines("")
    print_errors("====================================")
    print_errors("ERROR")
    print_errors("====================================")
    logging.error(e)
    print(e)