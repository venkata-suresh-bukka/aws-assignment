import boto3
import os
import json

ssm = boto3.client('ssm')
s3 = boto3.client('s3')

#Environment vaiables
SSM_ENV = os.environ['SSM_PARAMETER_NAME']
S3_BUCKET = os.environ['S3_BUCKET_NAME']
S3_KEY = os.environ.get('S3_KEY_NAME',)

def lambda_handler(event, context):
    try:
        # Fetch the SSM parameter
        parameter = ssm.get_parameter(Name=SSM_ENV)['Parameter']['Value']
        print("[INFO] STRING PARAMETER: " + parameter)
        
        # Store the response in S3
        response = s3.put_object(
            Bucket=S3_BUCKET,
            Key=S3_KEY,
            Body=json.dumps({SSM_ENV: parameter})
        )
        
        print("[INFO] Successfully stored parameter in S3: ", response)
        
        return {
            'statusCode': 200,
            'body': json.dumps('SSM Parameter stored in S3 successfully!')
        }
    except Exception as e:
        print("[ERROR] ", e)
        return {
            'statusCode': 500,
            'body': json.dumps('Failed to store SSM Parameter in S3')
        }
