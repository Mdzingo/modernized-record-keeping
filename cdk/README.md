# AWS CDK Deployment for Modernized Record Keeping API

This directory contains the AWS CDK infrastructure code for deploying the Modernized Record Keeping API to AWS Lambda with API Gateway and RDS PostgreSQL.

## Prerequisites

- AWS CLI configured with appropriate credentials
- Node.js 14.x or later
- AWS CDK v2 installed globally (`npm install -g aws-cdk`)
- Docker installed and running

## Deployment Steps

1. **Install dependencies**

```bash
npm install
```

2. **Bootstrap your AWS environment (if not already done)**

This step is required only once per AWS account/region:

```bash
cdk bootstrap
```

3. **Build the TypeScript code**

```bash
npm run build
```

4. **Deploy the stack**

```bash
cdk deploy
```

This will deploy the following resources:
- VPC with public and private subnets
- RDS PostgreSQL database
- Lambda function using Docker container
- API Gateway REST API

5. **View the outputs**

After deployment completes, the CDK will output:
- API Gateway URL for accessing your application
- RDS database endpoint

## Useful Commands

* `npm run build` - Compile TypeScript to JavaScript
* `npm run watch` - Watch for changes and compile
* `npm run test` - Perform the Jest unit tests
* `cdk deploy` - Deploy this stack to your default AWS account/region
* `cdk diff` - Compare deployed stack with current state
* `cdk synth` - Emits the synthesized CloudFormation template
* `cdk destroy` - Destroy the stack and all resources

## Customization

You can customize the deployment by modifying the `record-keeping-stack.ts` file:

- Change database instance type
- Adjust Lambda memory and timeout
- Modify VPC configuration
- Add additional AWS resources as needed
