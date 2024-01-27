from constructs import Construct
from aws_cdk import (
    RemovalPolicy,
    Stack,
    aws_iam as iam,
    aws_s3 as s3,
    aws_s3_deployment as s3_deployment,
    aws_cloudfront as cfn,
    aws_certificatemanager as acm,
)


class PersonalWebsite(Stack):

    def __init__(
            self,
            scope: Construct,
            construct_id: str,
            certificate_arn: str,
            domain_name: str,
            **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # A removal policiy should be added in production to protect the S3
        # bucket when deleting the stack.
        bucket: s3.Bucket = s3.Bucket(
            scope=self,
            id="s3-hosting",
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            access_control=s3.BucketAccessControl.PRIVATE,
            object_ownership=s3.ObjectOwnership.BUCKET_OWNER_ENFORCED,
            removal_policy=RemovalPolicy.DESTROY,
        )

        # OAI is a Legacy Access Identity and should be replaced with
        # Origin Access Control (OAC)
        oai: cfn.OriginAccessIdentity = cfn.OriginAccessIdentity(
            scope=self,
            id="oai-cfn",
        )
        bucket.add_to_resource_policy(iam.PolicyStatement(
            actions=["s3:GetObject"],
            resources=[bucket.arn_for_objects(key_pattern='*')],
            principals=[iam.CanonicalUserPrincipal(
                oai.cloud_front_origin_access_identity_s3_canonical_user_id)],
        ))
        # Reference certificate
        certificate = acm.Certificate.from_certificate_arn(
            self, "certificate", certificate_arn=certificate_arn
        )
        # Allow all should be changed to REDIRECT_TO_HTTPS later
        distribution = cfn.CloudFrontWebDistribution(
            scope=self,
            id="cfn-distribution",
            default_root_object="index.html",
            origin_configs=[cfn.SourceConfiguration(
                s3_origin_source=cfn.S3OriginConfig(
                    s3_bucket_source=bucket,
                    origin_access_identity=oai,
                ),
                behaviors=[cfn.Behavior(
                    is_default_behavior=True,
                    viewer_protocol_policy=cfn.ViewerProtocolPolicy.ALLOW_ALL,
                )]
            )],
            viewer_certificate=cfn.ViewerCertificate.from_acm_certificate(
                certificate=certificate,
                aliases=[domain_name],
                security_policy=cfn.SecurityPolicyProtocol.TLS_V1_2_2019,
                ssl_method=cfn.SSLMethod.SNI,
            )
        )

        # Deploy site contents to S3 bucket
        s3_deployment.BucketDeployment(
            scope=self,
            id="s3-deployment",
            sources=[s3_deployment.Source.asset("../dist")],
            destination_bucket=bucket,
            distribution=distribution,
            distribution_paths=["/*"],
        )
