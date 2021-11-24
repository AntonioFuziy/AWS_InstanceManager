import boto3
from botocore.config import Config
import time
import logging

from utils import print_errors, print_successes, print_lines

# def log_generator():
#   logging.basicConfig(filename='log.txt', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

#Specify us-east-1 North Virginia

def create_django(region, machine_id ,PUBLIC_POSTGRES_IP, security_group, ec2):
  django_script="""
  #cloud-config

  runcmd:
  - cd /home/ubuntu 
  - sudo apt update -y
  - echo "APT UPDATE" >> /home/ubuntu/log.txt
  - git clone https://github.com/AntonioFuziy/tasks
  - echo "GIT CLONE AntonioFuziy/tasks" >> /home/ubuntu/log.txt
  - cd tasks
  - echo "Entra em tasks" >> /home/ubuntu/log.txt
  - sed -i "s/node1/POSTGRES_IP/g" ./portfolio/settings.py
  - echo "CHANGING POSTGRES_IP" >> /home/ubuntu/log.txt
  - ./install.sh
  - echo "==========================================================" >> /home/ubuntu/log.txt
  - echo "RUNNING INSTALL" >> /home/ubuntu/log.txt
  - echo "==========================================================" >> /home/ubuntu/log.txt
  - sudo ufw allow 8080/tcp -y
  - echo "UFW 8080" >> /home/ubuntu/log.txt
  - sudo reboot
  - echo "REBOOTING" >> /home/ubuntu/log.txt
  """

  try:
    django_script = django_script.replace("POSTGRES_IP", str(PUBLIC_POSTGRES_IP))

    django_region = Config(region_name=region)
    django_resource = boto3.resource("ec2", config=django_region)

    django_instance = django_resource.create_instances(
      ImageId=machine_id,
      MinCount=1,
      MaxCount=1,
      InstanceType="t2.micro",
      KeyName="antonio.fuziy",
      SecurityGroupIds=[
        security_group.group_id
      ],
      TagSpecifications=[
        {
          "ResourceType": "instance",
          "Tags": [
            {
              "Key": "Name",
              "Value": "django"
            }
          ]
        }
      ],
      UserData=django_script
    )    
    print_lines("")
    print_lines("====================================")
    print_lines("Creating Django Instance...")
    django_instance[0].wait_until_running()
    django_instance[0].reload()
    waiting_time = 100
    waited_time = 0
    print_lines("Waiting for django to be ready...")
    while waited_time < waiting_time:
      print_lines("Waited for " + str(waited_time) + " seconds...")
      waited_time += 1
      time.sleep(1)
    print_successes("Djando Server Created!")

    all_north_virginia_instances = ec2.describe_instances()
    instances = all_north_virginia_instances["Reservations"]
    for instance in instances:
      for i in instance["Instances"]:
        if i["State"]["Name"] == "running":
          for tag in i["Tags"]:
            if tag["Value"] == "django":
              DJANGO_INSTANCE_ID = i["InstanceId"]
              print_successes(f"DJANGO_ID: {DJANGO_INSTANCE_ID}")

    return django_instance, DJANGO_INSTANCE_ID, django_instance[0].public_ip_address
  except Exception as e:
    print_lines("")
    print_errors("====================================")
    print_errors("ERROR")
    print_errors("====================================")
    print(e)
    return False