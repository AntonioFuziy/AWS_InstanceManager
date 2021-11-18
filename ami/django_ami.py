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

    print("")
    print("====================================")
    print("Creating Django AMI...")
    waiter.wait(ImageIds=[ami_instance['ImageId']])
    print("Djando AMI Created!")

    return ami_instance, ami_instance['ImageId']
  except Exception as e:
    print("")
    print("====================================")
    print("ERROR")
    print("====================================")
    print(e)
    return False
