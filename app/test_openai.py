# =====================================================
# OpenRouter AI Connectivity Test
# Autonomous AI DBA Operations Platform
# =====================================================

# Import required libraries
from openai import OpenAI
from dotenv import load_dotenv

import os
import httpx


# =====================================================
# LOAD ENVIRONMENT VARIABLES
# =====================================================

load_dotenv()


# =====================================================
# READ API KEY
# =====================================================

api_key = os.getenv(

    "OPENAI_API_KEY"
)


# =====================================================
# VALIDATE API KEY
# =====================================================

if not api_key:

    raise ValueError(

        "OPENAI_API_KEY not found in .env file"
    )


# =====================================================
# CREATE CUSTOM HTTP CLIENT
# SSL verification disabled temporarily
# =====================================================

http_client = httpx.Client(

    verify=False,

    timeout=60.0
)


# =====================================================
# CREATE OPENROUTER CLIENT
# =====================================================

client = OpenAI(

    api_key=api_key,

    base_url="https://openrouter.ai/api/v1",

    http_client=http_client,

    default_headers={

        "HTTP-Referer":
        "http://localhost",

        "X-Title":
        "Autonomous AI DBA Operations Platform"
    }
)


# =====================================================
# TEST AI CONNECTIVITY
# =====================================================

try:

    print("\n========================================")

    print(" OpenRouter AI Connectivity Test ")

    print("========================================\n")


    # =================================================
    # SEND TEST REQUEST
    # =================================================

    response = client.chat.completions.create(

        model="openai/gpt-4o-mini",

        messages=[

            {
                "role": "system",

                "content": """

                You are an expert SQL Server DBA
                and database reliability engineer.

                """
            },

            {
                "role": "user",

                "content": """

                Explain possible causes of SQL Server
                blocking in database environments.

                """
            }
        ]
    )


    # =================================================
    # DISPLAY AI RESPONSE
    # =================================================

    print("\nAI Response:\n")


    print(

        response.choices[0]
        .message.content

    )


    print("\n========================================")

    print(" AI Connectivity Test Successful ")

    print("========================================\n")


# =====================================================
# ERROR HANDLING
# =====================================================

except Exception as error:


    print("\n========================================")

    print(" AI Connectivity Test Failed ")

    print("========================================\n")


    print("Error occurred:\n")


    print(error)