#!/usr/bin/env python3

import aws_cdk as cdk

from cdk.cdk_stack import PersonalWebsite

app = cdk.App()
account_id = app.node.try_get_context("account_id")


PersonalWebsite(
    app,
    "portfolio-web-stack",
    certificate_arn="your_certificate_arn",
    domain_name="www.example.com",
)

app.synth()
