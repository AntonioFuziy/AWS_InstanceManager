from utils import print_errors, print_successes, print_lines

def create_auto_scalling(ec2_auto_scalling, ec2_north_virginia, target_group_arns):
  try:
    print_lines("")
    print_lines("====================================")
    print_lines("Launching auto scalling group...")
    list_all_zones = []
    all_zones = ec2_north_virginia.describe_availability_zones()
    for i in all_zones["AvailabilityZones"]:
      list_all_zones.append(i["ZoneName"])

    ec2_auto_scalling.create_auto_scaling_group(
      AutoScalingGroupName="auto_scaling_group",
      LaunchConfigurationName="ami_launched",
      MinSize=1,
      MaxSize=3,
      DesiredCapacity=1,
      DefaultCooldown=100,
      TargetGroupARNs=[target_group_arns],
      AvailabilityZones=list_all_zones
    )
    print_successes("Auto scalling group created")

  except Exception as e:
    print_lines("")
    print_errors("====================================")
    print_errors("Error creating Auto scalling group")
    print_errors("====================================")
    print(e)

def delete_auto_scalling(ec2):
  try:
    print_lines("")
    print_lines("====================================")
    print_lines("Deleting auto scalling group...")

    ec2.delete_auto_scaling_group(
      AutoScalingGroupName="auto_scaling_group",
      ForceDelete=True
    )
    print_successes("Auto scalling group deleted")

  except Exception as e:
    print_lines("")
    print_errors("====================================")
    print_errors("Error deleting Auto scalling group")
    print_errors("====================================")
    print(e)
