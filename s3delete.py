import os
import boto3
from dotenv import load_dotenv

load_dotenv()

# Establish the S3 client
s3 = boto3.client('s3',
                  aws_access_key_id=os.environ['S3_ACCESS_KEY'],
                  aws_secret_access_key=os.environ['S3_SECRET_KEY'],
                  endpoint_url=os.environ['S3_END_POINT']
                 )

bucket = os.environ['BUCKET']


def delete_file_from_bucket(bucket_name, file_name, s3_client):
    """Delete a file from the S3 bucket."""
    s3_client.delete_object(Bucket=bucket_name, Key=file_name)

def find_file_in_bucket(bucket_name, file_name, s3_client):
    """Find a file in the S3 bucket."""
    paginator = s3_client.get_paginator('list_objects_v2')
    for page in paginator.paginate(Bucket=bucket_name):
        if 'Contents' in page:
            for item in page['Contents']:
                if file_name in item['Key']:
                    return item['Key']
    return None

# Read the file names from the file
with open('files_to_delete.txt', 'r', encoding='utf-8') as file:
    files_to_delete = [line.strip() for line in file]

# Iterate over the list of files and delete each one if it is found in the bucket
for file_names in files_to_delete:
    found_file_name = find_file_in_bucket(bucket, file_names, s3)
    if found_file_name is not None:
        print(f'Found {found_file_name} in {bucket}')
        delete_confirmation = input("Do you want to delete it? [y/n] ")
        if delete_confirmation.lower() == 'y':
            delete_file_from_bucket(bucket, found_file_name, s3)
            print(f'Deleted {found_file_name} from {bucket}')
        else:
            print(f'Skipped deleting {found_file_name}')
    else:
        print(f'File {file_names} not found in {bucket}')
