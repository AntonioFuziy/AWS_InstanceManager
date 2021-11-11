#this command is used to check if you are authenticated to aws

import boto3
iam = boto3.client("iam")

for user in iam.list_users()["Users"]:
    print("")
    print(user["UserName"])
    print(user["UserId"])
    print(user["Arn"])
    print(user["CreateDate"])

with open("django.sh", "r") as f:
    run_postgres = f.read()
    db_ip = "192.168.0.0"
print(run_postgres.replace("s/node1/postgres_ip/g", f"s/node1/{db_ip}/g", 1))