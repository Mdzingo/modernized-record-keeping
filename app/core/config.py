import os
from dotenv import load_dotenv
from pathlib import Path
import boto3
import json
from botocore.exceptions import ClientError

# Load environment variables from .env file
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

def get_secret(secret_arn):
    """Get secret from AWS Secrets Manager"""
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager')
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_arn)
        secret = get_secret_value_response['SecretString']
        return json.loads(secret)
    except ClientError as e:
        raise e

class Settings:
    PROJECT_NAME: str = "Modernized Record Keeping API"
    PROJECT_VERSION: str = "1.0.0"
    
    # Database settings
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "recordsdb")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    # POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    secret_arn = os.environ['POSTGRES_SECRET_ARN']
    db_credentials = get_secret(secret_arn)
    POSTGRES_PASSWORD:str = db_credentials['password']
    

    
    SQLALCHEMY_DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )
    
    # API settings
    API_V1_STR: str = "/api/v1"

settings = Settings()
