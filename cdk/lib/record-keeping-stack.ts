import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as apigateway from 'aws-cdk-lib/aws-apigateway';
import * as rds from 'aws-cdk-lib/aws-rds';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as secretsmanager from 'aws-cdk-lib/aws-secretsmanager';
import * as path from 'path';

export class RecordKeepingStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Create a VPC for our resources
    const vpc = new ec2.Vpc(this, 'RecordKeepingVpc', {
      maxAzs: 2,
      natGateways: 1,
    });

    // Create a security group for the RDS instance
    const dbSecurityGroup = new ec2.SecurityGroup(this, 'DatabaseSecurityGroupV2', {
      vpc,
      description: 'Allow database connections',
      allowAllOutbound: true,
    });

    // Create a secret for database credentials
    const databaseCredentials = new secretsmanager.Secret(this, 'DBCredentialsV2', {
      secretName: 'modernized-record-keeping/db-credentials-v2',
      generateSecretString: {
        secretStringTemplate: JSON.stringify({ username: 'postgres' }),
        generateStringKey: 'password',
        excludePunctuation: true,
        includeSpace: false,
      },
    });

    // Create a PostgreSQL RDS instance
    const dbInstance = new rds.DatabaseInstance(this, 'RecordKeepingDatabaseV2', {
      engine: rds.DatabaseInstanceEngine.postgres({
        version: rds.PostgresEngineVersion.VER_14,
      }),
      instanceType: ec2.InstanceType.of(
        ec2.InstanceClass.BURSTABLE3,
        ec2.InstanceSize.MICRO,
      ),
      vpc,
      vpcSubnets: {
        subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS,
      },
      securityGroups: [dbSecurityGroup],
      credentials: rds.Credentials.fromSecret(databaseCredentials),
      databaseName: 'recordsdb',
      allocatedStorage: 20,
      maxAllocatedStorage: 100,
      backupRetention: cdk.Duration.days(7),
      deleteAutomatedBackups: true,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
    });

    // Allow Lambda security group to connect to the database
    dbSecurityGroup.addIngressRule(
      ec2.Peer.anyIpv4(),
      ec2.Port.tcp(5432),
      'Allow Lambda to connect to RDS'
    );

    // Create a Lambda function from Docker image
    const lambdaFunction = new lambda.DockerImageFunction(this, 'RecordKeepingLambda', {
      code: lambda.DockerImageCode.fromImageAsset(path.resolve(__dirname, '../../'), {
        exclude: ['cdk.out', 'cdk/cdk.out', '.git', 'node_modules']
      }),
      memorySize: 1024,
      timeout: cdk.Duration.seconds(30),
      vpc,
      vpcSubnets: {
        subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS,
      },
      environment: {
        POSTGRES_SERVER: dbInstance.dbInstanceEndpointAddress,
        POSTGRES_PORT: dbInstance.dbInstanceEndpointPort,
        POSTGRES_DB: 'recordsdb',
        POSTGRES_USER: 'postgres',
        POSTGRES_SECRET_ARN: databaseCredentials.secretArn,
      },
    });

    // Grant the Lambda function permission to read the secret
    databaseCredentials.grantRead(lambdaFunction);

    // Create an API Gateway REST API
    const api = new apigateway.LambdaRestApi(this, 'RecordKeepingApi', {
      handler: lambdaFunction,
      proxy: true,
      deployOptions: {
        stageName: 'prod',
        metricsEnabled: true,
        loggingLevel: apigateway.MethodLoggingLevel.INFO,
        dataTraceEnabled: true,
      },
    });

    // Output the API Gateway URL
    new cdk.CfnOutput(this, 'ApiUrl', {
      value: api.url,
      description: 'URL of the API Gateway endpoint',
    });

    // Output the database endpoint
    new cdk.CfnOutput(this, 'DatabaseEndpoint', {
      value: dbInstance.dbInstanceEndpointAddress,
      description: 'Endpoint of the RDS instance',
    });
  }
}
