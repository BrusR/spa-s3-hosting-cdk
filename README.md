# spa-s3-hosting-cdk
## Cdk initialization
In this tutorial, it is assumed that you have a succesfull installation of the 
CDK and the AWS CLI tools. Moreover you should have access to an AWS account and
have already set your credentials.

You create a new AWS CDK project by invoking "cdk init" in an empty directory. In 
this case the language I've chosen was python.
```
mkdir cdk
cd cdk
cdk init app --language python
```

Activate the virtual environment if not already activated.
```
source .venv/bin/activate
```

Then install the requirements.
```
python -m pip install -r requirements.txt
```

Bootstrap the CDK project just the first time. This creates the necessary
resources to deploy a CDK application.
```
cdk bootstrap
```

To list all available cdk stacks to deploy.
```
cdk list
```

To synthesize the application and get cloudformation output files.
```
cdk synthesize
```

To deploy to the cloud (this will deploy both the code and the cloud resources)
```
cdk deploy
```

# Cloud arquitecture
The cdk project deploys a single page application without a backend.The main AWS 
services it uses are S3 to store the files, Cloudfront to distribute the files and 
Cloudformation to build the stack.

![alt text](https://d1nm758bma1w92.cloudfront.net/github_images/SPA_architecture.png)