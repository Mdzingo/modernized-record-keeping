# Modernized Record Keeping API

A FastAPI application for managing records with CRUD operations.

## Features

- Built with FastAPI and Python 3.12
- Poetry for dependency management
- SQLAlchemy ORM for database operations
- Full CRUD operations for records
- PostgreSQL database (configurable via environment variables)

## Record Format

```json
{
  "things_stored": "{ 1: { thing_attribute: attribute } }",
  "timestamp": 1529729125
}
```

## Installation

1. Clone the repository
2. Install dependencies with Poetry:

```bash
poetry install
```

## Database Setup

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

## Running the Application

```bash
poetry run python -m app.main
```

Or use Uvicorn directly:

```bash
poetry run uvicorn app.main:app --reload
```

## API Endpoints

- `GET /api/v1/records/`: List all records
- `POST /api/v1/records/`: Create a new record
- `GET /api/v1/records/{record_id}`: Get a specific record
- `PUT /api/v1/records/{record_id}`: Update a record
- `DELETE /api/v1/records/{record_id}`: Delete a record

## API Documentation

Once the application is running, you can access the auto-generated API documentation at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`