# Modernized Record Keeping API

A FastAPI application for managing records with CRUD operations, deployable both locally and to AWS Lambda.

## Features

- Built with FastAPI and Python 3.12
- Poetry for dependency management
- SQLAlchemy ORM for database operations
- Full CRUD operations for records
- PostgreSQL database (configurable via environment variables)
- AWS Lambda deployment using Docker and CDK

## Record Format

```json
{
  "things_stored": "{ 1: { thing_attribute: attribute } }",
  "timestamp": 1529729125
}
```

## Local Development

### Installation

1. Clone the repository
2. Install dependencies with Poetry:

```bash
poetry install
```

### Database Setup

The application uses PostgreSQL. Make sure you have PostgreSQL installed and running locally.

1. Create a database for the application:

```bash
createdb recordsdb
```

2. Configure the database connection in the `.env` file:

```
POSTGRES_SERVER=localhost
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=recordsdb
POSTGRES_PORT=5432
```

### Running the Application Locally

```bash
poetry run python -m app.main
```

Or use Uvicorn directly:

```bash
poetry run uvicorn app.main:app --reload
```

You can also use the provided start script:

```bash
./scripts/start_app.sh
```

## AWS Lambda Deployment

This application can be deployed to AWS Lambda using Docker and AWS CDK.

### Prerequisites

- AWS CLI configured with appropriate credentials
- Node.js 14.x or later
- AWS CDK v2 installed globally (`npm install -g aws-cdk`)
- Docker installed and running

### Deployment Steps

1. Navigate to the CDK directory:

```bash
cd cdk
```

2. Install dependencies:

```bash
npm install
```

3. Bootstrap your AWS environment (if not already done):

```bash
cdk bootstrap
```

4. Build the TypeScript code:

```bash
npm run build
```

5. Deploy the stack:

```bash
cdk deploy
```

This will deploy:
- VPC with public and private subnets
- RDS PostgreSQL database
- Lambda function using Docker container
- API Gateway REST API

After deployment completes, the CDK will output:
- API Gateway URL for accessing your application
- RDS database endpoint

## API Endpoints

- `GET /api/v1/records/`: List all records
- `POST /api/v1/records/`: Create a new record
- `GET /api/v1/records/{record_id}`: Get a specific record
- `PUT /api/v1/records/{record_id}`: Update a record
- `DELETE /api/v1/records/{record_id}`: Delete a record

## API Documentation

Once the application is running, you can access the auto-generated API documentation at:

- Swagger UI: `http://localhost:8000/docs` (local) or `https://{api-id}.execute-api.{region}.amazonaws.com/prod/docs` (AWS)
- ReDoc: `http://localhost:8000/redoc` (local) or `https://{api-id}.execute-api.{region}.amazonaws.com/prod/redoc` (AWS)