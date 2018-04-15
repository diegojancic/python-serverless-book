import boto3

ses = boto3.client("ses")

response = ses.send_email(
    Source='noreply@company.com',
    Destination={
        'ToAddresses': ['recipient@company.com',],
    },
    Message={
        'Subject': {
            'Data': 'Hello from AWS!'
        },
        'Body': {
            'Text': {
                'Data': 'Message body goes here'
            }
        }
    },
)

print(response["ResponseMetadata"]["HTTPStatusCode"])

"""
Sample response:
{'MessageId': '01000162c6466689-eaacb226-6a48-4dc8-bed1-000000000000-000000', 'ResponseMetadata': {'HTTPStatusCode': 200, 'RetryAttempts': 0, 'RequestId': '318660bb-4033-11e8-9ddf-5b5c2f092974', 'HTTPHeaders': {'date': 'Sat, 14 Apr 2018 22:28:44 GMT', 'content-length': '326', 'x-amzn-requestid': '318660bb-4033-11e8-9ddf-5b5c2f092974', 'content-type': 'text/xml'}}}

"""
