#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cdk.cdk import CdkApiStack




app = cdk.App()
CdkApiStack(app, "CdkApiStack")

app.synth()