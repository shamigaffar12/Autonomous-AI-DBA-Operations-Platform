# Import required libraries
"""
from openai import OpenAI
from dotenv import load_dotenv
import os


# Load environment variables
load_dotenv()


# Read API key
api_key = os.getenv("OPENAI_API_KEY")


# Create OpenAI client
client = OpenAI(api_key=api_key)


try:

    # Send test request
    response = client.chat.completions.create(

        model="gpt-4o-mini",

        messages=[
            {
                "role": "user",
                "content": "What causes SQL Server blocking?"
            }
        ]
    )

    # Print response
    print("\nAI Response:\n")
    print(response.choices[0].message.content)

except Exception as error:

    print("\nError occurred:")
    print(error)
"""

# =====================================================
# OpenRouter AI Connectivity Test
# Autonomous AI DBA Operations Platform
# =====================================================

# Import required libraries
from openai import OpenAI
from dotenv import load_dotenv
import os
import httpx


# Load environment variables
load_dotenv()


# Read API key
api_key = os.getenv("OPENAI_API_KEY")


# Create custom HTTP client
# SSL verification disabled temporarily
http_client = httpx.Client(

    verify=False,

    timeout=60.0
)


# Create OpenAI-compatible client
client = OpenAI(

    api_key=api_key,

    base_url="https://openrouter.ai/api/v1",

    http_client=http_client
)


try:

    print("\nTesting OpenRouter AI connectivity...\n")


    # Send request
    response = client.chat.completions.create(

        model="openai/gpt-4o-mini",

        messages=[

            {
                "role": "user",

                "content": """
                Explain possible causes of SQL Server blocking
                in database environments.
                """
            }
        ]
    )


    print("\nAI Response:\n")

    print(response.choices[0].message.content)


except Exception as error:

    print("\nError occurred:\n")

    print(error)