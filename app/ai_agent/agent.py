# =========================================================
# AI DBA Agent
# Autonomous AI DBA Operations Platform
# =========================================================

# Import OpenAI SDK
from openai import OpenAI

# Import environment variable support
from dotenv import load_dotenv

# Import OS module
import os

# Import HTTPX
import httpx


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()


# =========================================================
# AI DBA AGENT CLASS
# =========================================================

class AIDBAgent:


    # =====================================================
    # CONSTRUCTOR
    # =====================================================

    def __init__(self):

        # AI Agent Name
        self.name = "Autonomous AI DBA Agent"


        # =================================================
        # LOAD API KEY
        # =================================================

        api_key = os.getenv(

            "OPENAI_API_KEY"
        )


        # =================================================
        # VALIDATE API KEY
        # =================================================

        if not api_key:

            raise ValueError(

                "OPENAI_API_KEY not found in .env file"

            )


        # =================================================
        # CUSTOM HTTP CLIENT
        # =================================================

        http_client = httpx.Client(

            verify=False,

            timeout=60.0
        )


        # =================================================
        # OPENROUTER CLIENT CONFIGURATION
        # =================================================

        self.client = OpenAI(

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
    # INCIDENT ANALYSIS FUNCTION
    # =====================================================

    def analyze_incident(self, incident):

        """
        Analyze SQL incident using AI.
        """

        try:

            print("\nGenerating AI Incident Analysis...\n")


            # =============================================
            # SEND INCIDENT TO AI MODEL
            # =============================================

            response = self.client.chat.completions.create(

                model="openai/gpt-4o-mini",

                messages=[

                    {
                        "role": "system",

                        "content": """

                        You are an expert SQL Server DBA
                        and database reliability engineer.

                        Analyze the SQL incident and generate:

                        1. Incident Summary
                        2. Root Cause Analysis
                        3. Risk Assessment
                        4. Recommended Actions
                        5. Prevention Recommendations

                        Provide response in professional
                        enterprise operational format.

                        """
                    },

                    {
                        "role": "user",

                        "content": incident
                    }
                ]
            )


            # =============================================
            # EXTRACT AI RESPONSE
            # =============================================

            ai_analysis = (

                response.choices[0]
                .message.content

            )


            # =============================================
            # RETURN AI RESPONSE
            # =============================================

            return {

                "incident": incident,

                "analysis": ai_analysis
            }


        # ================================================
        # FALLBACK RESPONSE
        # ================================================

        except Exception as error:


            print(f"\nAI Connection Error: {error}\n")


            fallback_response = """

Incident Summary:
High resource utilization detected in SQL Server.

Root Cause Analysis:
Possible CPU-intensive query execution or workload spike identified.

Risk Assessment:
Medium operational impact observed.

Recommended Actions:
- Review active sessions
- Analyze expensive queries
- Check indexing and execution plans
- Monitor blocking and wait statistics

Prevention Recommendations:
- Implement proactive monitoring
- Configure alert thresholds
- Perform regular performance tuning

"""


            return {

                "incident": incident,

                "analysis": fallback_response
            }


# =========================================================
# MAIN EXECUTION BLOCK
# =========================================================

if __name__ == "__main__":


    print("\n========================================")

    print(" Autonomous AI DBA Operations Platform ")

    print(" AI DBA Agent ")

    print("========================================\n")


    # =====================================================
    # CREATE AI AGENT OBJECT
    # =====================================================

    agent = AIDBAgent()


    # =====================================================
    # SAMPLE INCIDENT DATA
    # =====================================================

    incident_data = """

    SQL Monitoring Alert:

    - High CPU usage detected
    - Blocking session identified
    - Long running query detected
    - Database response time increased
    - Query timeout reported by application
    - CPU utilization exceeded threshold

    """


    # =====================================================
    # RUN AI INCIDENT ANALYSIS
    # =====================================================

    result = agent.analyze_incident(

        incident_data

    )


    # =====================================================
    # DISPLAY AI OUTPUT
    # =====================================================

    print("\n========================================")

    print(" AI INCIDENT ANALYSIS REPORT ")

    print("========================================\n")


    print(result["analysis"])


    # =====================================================
    # CREATE REPORTS FOLDER
    # =====================================================

    os.makedirs(

        "reports",

        exist_ok=True
    )


    # =====================================================
    # SAVE INCIDENT REPORT
    # =====================================================

    with open(

        "reports/incident_report.txt",

        "w",

        encoding="utf-8"

    ) as report_file:


        report_file.write(

            result["analysis"]

        )


    # =====================================================
    # SUCCESS MESSAGE
    # =====================================================

    print("\n========================================")

    print(" Incident report saved successfully ")

    print("========================================\n")