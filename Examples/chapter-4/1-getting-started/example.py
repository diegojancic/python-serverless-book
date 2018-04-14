import boto3

iam = boto3.client("iam")
print(iam.get_user())
print()
print(iam.get_user()["User"]["UserName"])