
aws iam create-role --role-name lambda_send_email_role \
					--assume-role-policy-document file://assume-role-policy.json
# OUTPUT:
# {
#     "Role": {
#         "CreateDate": "2018-04-18T21:52:37.497Z",
#         "RoleName": "lambda_send_email_role",
#         "RoleId": "AROAIXXXXXXXXXXXXXXXX",
#         "Arn": "arn:aws:iam::532000000000:role/lambda_send_email_role",
#         "Path": "/",
#         "AssumeRolePolicyDocument": {
#             "Version": "2012-10-17",
#             "Statement": {
#                 "Principal": {
#                     "Service": "lambda.amazonaws.com"
#                 },
#                 "Effect": "Allow",
#                 "Action": "sts:AssumeRole"
#             }
#         }
#     }
# }

aws iam put-role-policy --role-name lambda_send_email_role \
						--policy-name SES_Send_Email \
						--policy-document file://role-policy.json

# Remove existent ZIP file and compress the function 
rm -f say_hi.zip && zip say_hi.zip say_hi.py

# Get role ARN:
aws iam get-role --role-name lambda_send_email_role

aws lambda create-function --function-name say_hi \
							--runtime python3.6 \
							--role arn:aws:iam::532000000000:role/lambda_send_email_role \
							--handler say_hi.lambda_handler \
							--timeout 10 \
							--publish \
							--zip-file fileb://say_hi.zip \
							--environment Variables="{FROM_ADDRESS=from_address@company.com,TO_ADDRESS=to_address@company.com}"
