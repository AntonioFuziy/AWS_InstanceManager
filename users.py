#this command is used to check if you are authenticated to aws

import boto3 
from botocore.config import Config
from pprint import pprint

# north = Config(region_name="us-east-2")
ec2_r2 = boto3.client('ec2', region_name="us-east-1")
existing_images = ec2_r2.describe_images(Owners=["self"])
if len(existing_images["Images"]) > 0:
    for image in existing_images["Images"]:
        if image["Name"] == "django_AMI":
            print(image["ImageId"])
            print(image["Name"])
        # print(image)
# delete_instances_ids = []
# existing_instances = ec2_r2.describe_instances()
# existing_instances = existing_instances["Reservations"]
# for instance in existing_instances:
#     for i in instance["Instances"]:
#         print(i["State"]["Name"])
#         if i["State"]["Name"]  == "running":
#             for tag in i["Tags"]:
#                 if tag["Value"] == "postgres":
#                     print(i["InstanceId"])


# existing_security_groups = ec2_r2.describe_security_groups()
# for security_group in existing_security_groups["SecurityGroups"]:
#     print(security_group["GroupId"])