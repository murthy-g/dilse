import os
import boto3
from aws_cdk import (
    Stack,
    aws_apigateway as apigateway,
    aws_lambda as _lambda,
    aws_iam as _iam,
    aws_s3 as s3,
    aws_logs as logs,
    # core,
    aws_dynamodb as ddb
    # aws_s3_deployment as s3deploy,
)

from constructs import Construct

class CdkApiStack(Stack):

    def get_all_keys_from_s3_bucket(bucket_name):
        s3_client = boto3.client('s3')
        
        keys = []
        continuation_token = None

        while True:
            list_objects_kwargs = {'Bucket': bucket_name}
            if continuation_token:
                list_objects_kwargs['ContinuationToken'] = continuation_token

            response = s3_client.list_objects_v2(**list_objects_kwargs)

            if 'Contents' in response:
                for obj in response['Contents']:
                    keys.append(obj['Key'])

            if not response.get('IsTruncated'):  # Once all keys are fetched
                break

            continuation_token = response.get('NextContinuationToken')

        return keys

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

    
        #create layers from backend/layers/layers/layers.zip
        layers = _lambda.LayerVersion(
            self,
            "layers",
            code=_lambda.Code.from_asset("layers/layers/layers.zip"),
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_8],
            description="layers",
        )

        # packages = _lambda.LayerVersion(
        #     self,
        #     "packages",
        #     code=_lambda.Code.from_asset("layers/layers/packages.zip"),
        #     compatible_runtimes=[_lambda.Runtime.PYTHON_3_8],
        #     description="packages",
        # )
        
        # users_table = ddb.Table(
        #     self, "UsersTable",
        #     partition_key=ddb.Attribute(name="user_id", type=ddb.AttributeType.STRING),
        #     # other table settings...
        # )

        # matches_table = ddb.Table(
        #     self, "MatchesTable",
        #     partition_key=ddb.Attribute(name="user_id", type=ddb.AttributeType.STRING),
        #     # other table settings...
        # )
        
        
        #create s3 bucket
        bucket = s3.Bucket(self, "dilse_bucket")
        #create iam role to write files into s3 bucket from lambda function
        dilse_lambda_role = _iam.Role(
            self,
            "DilseRole",
            assumed_by=_iam.ServicePrincipal("lambda.amazonaws.com"),
        )

        #attach created iam role to lambda function
        dilse_lambda_role.add_to_policy(
            _iam.PolicyStatement(
                actions=["s3:PutObject", "s3:GetObject"],
                resources=[bucket.bucket_arn + "/*"],
            )
        )

        dilse_lambda_role.add_to_policy(
            _iam.PolicyStatement(
                actions=["dynamodb:Query", "dynamodb:PutItem", "dynamodb:GetItem", "dynamodb:UpdateItem", "dynamodb:DeleteItem", "dynamodb:Scan"],
                resources=[
                    f"arn:aws:dynamodb:us-east-1:897527378750:table/users",
                    f"arn:aws:dynamodb:us-east-1:897527378750:table/users/index/EmailIndex"
                ]
            )
        )


        #create lambda function
        login_lambda = _lambda.Function(
            self,
            "LoginHandler",
            runtime=_lambda.Runtime.PYTHON_3_8,
            code=_lambda.Code.from_asset("handlers"),
            handler="lambda_login.lambda_login",
            layers=[layers],
            role=dilse_lambda_role,
        )

        register_lambda = _lambda.Function(
            self,
            "RegisterHandler",
            runtime=_lambda.Runtime.PYTHON_3_8,
            code=_lambda.Code.from_asset("handlers"),
            handler="lambda_register.lambda_register",
            layers=[layers],
            role=dilse_lambda_role,
        )

        like_lambda = _lambda.Function(
            self,
            "LikeHandler",
            runtime=_lambda.Runtime.PYTHON_3_8,
            code=_lambda.Code.from_asset("handlers"),
            handler="lambda_like.lambda_like",
            layers=[layers],
            role=dilse_lambda_role,
        )

        match_lambda = _lambda.Function(
            self,
            "MatchHandler",
            runtime=_lambda.Runtime.PYTHON_3_8,
            code=_lambda.Code.from_asset("handlers"),
            handler="lambda_getMatches.get_matches",
            layers=[layers],
            role=dilse_lambda_role,
        )

        getphotos_lambda = _lambda.Function(
            self,
            "GetPhotosHandler",
            runtime=_lambda.Runtime.PYTHON_3_8,
            code=_lambda.Code.from_asset("handlers"),
            handler="lambda_getPhotos.get_photos",
            layers=[layers],
            role=dilse_lambda_role,
        )

        fileupload_lambda = _lambda.Function(
            self,
            "FileUploadHandler",
            runtime=_lambda.Runtime.PYTHON_3_8,
            code=_lambda.Code.from_asset("handlers"),
            handler="lambda_fileUpload.upload_file",
            layers=[layers],
            role=dilse_lambda_role,
        )

        recommendations_lambda = _lambda.Function(
            self,
            "RecommendationsHandler",
            runtime=_lambda.Runtime.PYTHON_3_8,
            code=_lambda.Code.from_asset("handlers"),
            handler="lambda_getrecommendations.get_recommendations",
            layers=[layers],
            role=dilse_lambda_role,
        )

        #create api gateway
        api = apigateway.RestApi(
            self,
            "DilSeApi",
            rest_api_name="DilSeApi",
            description="This service generates audio from text",
            )
        
        #create api gateway lambda integration
        login_lambda_integration = apigateway.LambdaIntegration(login_lambda)
        register_lambda_integration = apigateway.LambdaIntegration(register_lambda)
        like_lambda_integration = apigateway.LambdaIntegration(like_lambda)
        match_lambda_integration = apigateway.LambdaIntegration(match_lambda)
        fileupload_lambda_integration = apigateway.LambdaIntegration(fileupload_lambda)
        getphotos_lambda_integration = apigateway.LambdaIntegration(getphotos_lambda)
        recommendations_lambda_integration = apigateway.LambdaIntegration(recommendations_lambda)


        #create api gateway resource
        api.root.add_resource("login").add_method("POST", login_lambda_integration)
        api.root.add_resource("register").add_method("POST", register_lambda_integration)
        api.root.add_resource("like").add_method("POST", like_lambda_integration)
        api.root.add_resource("match").add_method("GET", match_lambda_integration)
        api.root.add_resource("upload").add_method("POST", fileupload_lambda_integration)
        api.root.add_resource("getphotos").add_method("GET", getphotos_lambda_integration)
        api.root.add_resource("recommendations").add_method("GET", recommendations_lambda_integration)

        
        log_group = logs.LogGroup(self, "ApiGatewayAccessLogs")

        api_gateway_logging_role = _iam.Role(
            self,
            "DilSeRole",
            assumed_by=_iam.ServicePrincipal("apigateway.amazonaws.com"),
        )

        api_gateway_logging_role.add_to_policy(
            _iam.PolicyStatement(
                actions=["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"],
                resources=[log_group.log_group_arn]
            )
        )
