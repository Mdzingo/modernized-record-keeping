#!/usr/bin/env python
"""
Script to test PostgreSQL database connection.
This helps verify that the database configuration is correct.
"""

import sys
import os
import logging
from pathlib import Path

# Add the parent directory to sys.path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import create_engine, text
from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_connection():
    """Test the connection to the PostgreSQL database."""
    try:
        # Create engine with the configured database URL
        logger.info(f"Attempting to connect to database at: {settings.SQLALCHEMY_DATABASE_URL}")
        engine = create_engine(settings.SQLALCHEMY_DATABASE_URL)
        
        # Try to connect and execute a simple query
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            for row in result:
                logger.info(f"Connection successful! Test query result: {row[0]}")
        
        logger.info("Database connection test completed successfully!")
        return True
    except Exception as e:
        logger.error(f"Error connecting to database: {e}")
        return False

if __name__ == "__main__":
    logger.info("Testing database connection...")
    success = test_connection()
    
    if success:
        logger.info("✅ Database connection is working correctly!")
        sys.exit(0)
    else:
        logger.error("❌ Failed to connect to the database. Please check your configuration.")
        sys.exit(1)
