import json
import boto3

def lambda_handler(event, context):
    # Triggered by new file in S3 bucket
    s3 = boto3.client('s3')
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    # Read file
    response = s3.get_object(Bucket=bucket, Key=key)
    content = response['Body'].read().decode('utf-8')

    # Simple transformation: uppercase all lines
    transformed = [line.upper() for line in content.splitlines()]

    output_key = key.replace('input/', 'output/')
    s3.put_object(
        Bucket='your-output-bucket',
        Key=output_key,
        Body='\n'.join(transformed).encode('utf-8')
    )

    return {
        'statusCode': 200,
        'body': json.dumps(f'Processed {key} and saved to {output_key}')
    }