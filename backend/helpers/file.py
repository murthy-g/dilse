ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
S3_BUCKET = 'profile_images'
import boto3

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_to_s3(file, bucket_name, acl="public-read"):
    s3 = boto3.client('s3', aws_access_key_id='YOUR_AWS_ACCESS_KEY',
                      aws_secret_access_key='YOUR_AWS_SECRET_KEY')
    try:
        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )
    except Exception as e:
        print("Something Happened: ", e)
        # handle any errors here
        return False
    return True