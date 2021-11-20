import boto3
from botocore.config import Config

from utils import print_errors, print_successes, print_lines

#Specify us-east-1 North Virginia

def create_django(region, machine_id ,PUBLIC_POSTGRES_IP, security_group, ec2):
  try:
    with open("django.sh", "r") as f:
      django_file = f.read()
      run_django = django_file.replace("s/node1/postgres_ip/g", f"s/node1/{PUBLIC_POSTGRES_IP}/g", 1)

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
      UserData=run_django
    )    
    print_lines("")
    print_lines("====================================")
    print_lines("Creating Django Instance...")
    django_instance[0].wait_until_running()
    django_instance[0].reload()
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