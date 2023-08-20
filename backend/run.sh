# setup python virtual environment
python3 -m venv venv
source venv/bin/activate

source venv/bin/activate
pip install --upgrade pip
pip install --upgrade aws-cdk.core aws-cdk.aws-apigateway aws-cdk.aws-lambda aws-cdk.aws-s3 aws-cdk.aws-s3-deployment boto3 Flask
pip install -r requirements.txt
pip install aws-cdk-lib==2.90.0
pip install constructs==10.2.69
pip install --upgrade aws-cdk-lib
