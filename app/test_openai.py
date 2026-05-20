import os
import logging
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

try:
    # Read API key
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in .env file")

    logger.info("API key loaded successfully")

    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)

    logger.info("OpenAI client initialized")

    # Test API request
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": "Reply only with: AI DBA environment test successful"
            }
        ]
    )

    logger.info("OpenAI API connection successful")

    print("\nAI RESPONSE:")
    print(response.choices[0].message.content)

except Exception as e:
    logger.error(f"Error occurred: {e}")

# SQL placeholder
logger.info("SQL connectivity placeholder initialized")

print("\nEnvironment verification completed successfully.")