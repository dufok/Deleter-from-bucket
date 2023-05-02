import boto3
import os

s3 = boto3.client('s3',
                    aws_access_key_id=os.environ['S3_ACCESS_KEY'],
                    aws_secret_access_key=os.environ['S3_SECRET_KEY'],
                     )

bucket = os.environ['BUCKET']

def delete_file_from_bucket(client, bucket, file_name_to_delete):
    # List all objects in the bucket
    response = client.list_objects_v2(Bucket=bucket)
    objects = response.get('Contents', [])

    # Iterate through the objects
    for obj in objects:
        if obj['Key'] == file_name_to_delete:
            # If the object's Key matches the file_name_to_delete, delete it
            client.delete_object(Bucket=bucket, Key=obj['Key'])
            print(f"Deleted file {file_name_to_delete} from {bucket}")
            return
    print(f"File {file_name_to_delete} not found in {bucket}")

# Replace 'your_specific_file_name.ext' with the name of the file you want to delete
file_name_to_delete = "your_specific_file_name.ext"
delete_file_from_bucket(s3, bucket, file_name_to_delete)