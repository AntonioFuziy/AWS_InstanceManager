from utils import print_errors, print_successes, print_lines

def launch_ami(ec2, image_id, security_group):
  try:
    print_lines("")
    print_lines("====================================")
    print_lines("Launching AMI...")
    ec2.create_launch_configuration(
      LaunchConfigurationName='ami_launched',
      ImageId=image_id,
      SecurityGroups=[
        security_group.group_id
      ],
      InstanceType='t2.micro'
    )
    print_successes("AMI Launched")
  except Exception as e:
    print_lines("")
    print_errors("====================================")
    print_errors("Error launching AMI")
    print_errors("====================================")
    print(e)
  
def delete_launch_ami(ec2):
  try:
    print_lines("")
    print_lines("====================================")
    print_lines("Deleting Launch Configuration...")
    ec2.delete_launch_configuration(LaunchConfigurationName="ami_launched")
    print_successes("Launch Configuration Deleted...")
  except Exception as e:
    print_lines("")
    print_errors("====================================")
    print_errors("Error deleting Launch Configuration")
    print_errors("====================================")
    print(e)