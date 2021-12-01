from utils import print_errors, print_successes, print_lines, print_warnings
from log import logging

def launch_ami(ec2, image_id, security_group):
  try:
    print_lines("")
    print_lines("====================================")
    print_lines("Launching AMI...")
    logging.info("Launching AMI...")

    ec2.create_launch_configuration(
      LaunchConfigurationName="ami_launched",
      ImageId=image_id,
      SecurityGroups=[
        security_group.group_id
      ],
      InstanceType='t2.micro',
      KeyName="antonio.fuziy"
    )

    print_successes("AMI Launched")
    logging.info("AMI Launched")

  except Exception as e:
    print_lines("")
    print_errors("====================================")
    print_errors("Error launching AMI")
    print_errors("====================================")
    logging.error(e)
    print(e)
  
def delete_launch_ami(ec2):
  try:
    print_lines("")
    print_lines("====================================")
    print_lines("Deleting Launch Configuration...")
    logging.info("Deleting Lauch Configuration...")

    ec2.delete_launch_configuration(LaunchConfigurationName="ami_launched")
    
    print_successes("Launch Configuration Deleted")
    logging.info("Launch Configuration Deleted")
    
  except:
    print_lines("")
    print_warnings("====================================")
    print_warnings("Launch Configuration not found")
    print_warnings("====================================")
    logging.warning("Launch Configuration not found")