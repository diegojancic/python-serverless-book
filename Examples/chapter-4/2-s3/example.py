import boto3

s3 = boto3.client("s3")
bucket_name = "learning-serverless-ireland-bucket"

s3.upload_file('hello_world.txt', bucket_name, "chapter-4/hello_world.txt")
response = s3.list_objects(Bucket=bucket_name)
files = response["Contents"]
print ([f["Key"] for f in files])
