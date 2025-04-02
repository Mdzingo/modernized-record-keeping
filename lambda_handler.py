import json
import logging
from mangum import Mangum

from app.main import app

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Create Mangum handler for Lambda
handler = Mangum(app)

# You can add additional Lambda-specific code here if needed
def log_event(event):
    """Log the Lambda event for debugging purposes."""
    logger.info(f"Event: {json.dumps(event)}")
