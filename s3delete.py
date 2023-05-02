import os
import boto3

from dotenv import load_dotenv



# Load the environment variables from the .env file
load_dotenv()

# Now you can access the environment variables using os.getenv
s3 = boto3.client('s3',
                  aws_access_key_id=os.getenv('S3_ACCESS_KEY'),
                  aws_secret_access_key=os.getenv('S3_SECRET_KEY'),
                 )

bucket = os.getenv('BUCKET')

# Function to delete a file from a bucket
def delete_file_from_bucket(bucket_name, file_name, s3_client):
    s3_client.delete_object(
        Bucket=bucket_name,
        Key=file_name
    )

# Function to find a file in a bucket
def find_file_in_bucket(bucket_name, file_name, s3_client):
    response = s3_client.list_objects_v2(
        Bucket=bucket_name,
    )

    for item in response['Contents']:
        if file_name in item['Key']:
            return item['Key']
    return None

# Read the file names from the file
with open('files_to_delete.txt', 'r') as file:
    files_to_delete = [line.strip() for line in file]

# Iterate over the list of files and delete each one if it is found in the bucket
for file_name in files_to_delete:
    found_file_name = find_file_in_bucket(bucket, file_name, s3)
    if found_file_name is not None:
        delete_file_from_bucket(bucket, found_file_name, s3)
        print(f'Deleted {found_file_name} from {bucket}')
    else:
        print(f'File {file_name} not found in {bucket}')
