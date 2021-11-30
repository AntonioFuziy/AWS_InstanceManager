from utils import print_errors, print_successes, print_lines
from log import logging

def create_django_AMI(ec2, DJANGO_INSTANCE_ID, waiter):
  try:
    ami_instance = ec2.create_image(
      Name="django_AMI",
      InstanceId=DJANGO_INSTANCE_ID,
      NoReboot=False,
      TagSpecifications=[
        {
          "ResourceType": "image",
          "Tags": [
            {
              "Key": "Name",
              "Value": "django_image"
            }
          ]
        }
      ]
    )

    print_lines("")
    print_lines("====================================")
    print_lines("Creating Django AMI...")
    logging.info("Creating Django AMI...")
    waiter.wait(ImageIds=[ami_instance['ImageId']])
    print_successes("Djando AMI Created!")
    logging.info("Django AMI Created")

    return ami_instance, ami_instance['ImageId']
    
  except Exception as e:
    print_lines("")
    print_errors("====================================")
    print_errors("ERROR")
    print_errors("====================================")
    logging.error(e)
    print(e)
    return False
