import boto3
from botocore.config import Config

#Specify us-east-1 North Virginia

def create_django(region, machine_id ,public_ip_postgres, security_group):
  try:
    with open("django.sh", "r") as f:
      django_file = f.read()
      run_django = django_file.replace("s/node1/postgres_ip/g", f"s/node1/{public_ip_postgres}/g", 1)

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
    print("")
    print("Creating Django Instance...")
    django_instance[0].wait_until_running()
    django_instance[0].reload()

    print("")
    print("Djando Server Created!")
    return django_instance
  except Exception as e:
    print(e)
    return False