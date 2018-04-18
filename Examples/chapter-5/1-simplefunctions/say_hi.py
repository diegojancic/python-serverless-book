import boto3
import os

def lambda_handler(event, context):
    from_address = os.environ["FROM_ADDRESS"]
    to_address = os.environ["TO_ADDRESS"]

    ses = boto3.client("ses")
    response = ses.send_email(
        Source=from_address,
        Destination={
            'ToAddresses': [to_address,],
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
