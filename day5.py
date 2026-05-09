import boto3

# Connect to IAM
iam = boto3.client('iam')

# Get your own user info
user = iam.get_user()
print("Connected as:", user['User']['UserName'])
print("Account ARN:", user['User']['Arn'])

# Connect to S3
s3 = boto3.client('s3')

# List all buckets
response = s3.list_buckets()

print("\nYour S3 Buckets:")
if response['Buckets']:
    for bucket in response['Buckets']:
        print(" -", bucket['Name'])
else:
    print("No buckets yet!")

# Create bucket only if not exists
bucket_name = "sonal-boto3"
existing_buckets = [b['Name'] for b in response['Buckets']]

if bucket_name not in existing_buckets:
    s3.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={
            'LocationConstraint': 'ap-south-1'
        }
    )
    print(f"\nBucket created: {bucket_name} ✅")
else:
    print(f"\nBucket already exists: {bucket_name} ✅")

# Upload a file to S3
s3.upload_file(
    'test.txt',           # file on your laptop
    bucket_name,          # your bucket name
    'test.txt'            # name it will have in S3
)

print(f"\nFile uploaded to: {bucket_name}/test.txt ✅")

# List files in bucket
print(f"\nFiles in {bucket_name}:")
objects = s3.list_objects_v2(Bucket=bucket_name)
for obj in objects['Contents']:
    print(" -", obj['Key'])
