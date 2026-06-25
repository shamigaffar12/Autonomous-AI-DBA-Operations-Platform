# =========================================================
# Teams Notifier
# Autonomous AI DBA Operations Platform
# =========================================================

import json
import os
import urllib.request


def send_teams_alert(
    message: str,
    title: str = "AI DBA Platform Alert"
) -> bool:

    webhook_url = os.getenv(
        "TEAMS_WEBHOOK_URL",
        ""
    ).strip()

    if not webhook_url:

        print("\n========================================")
        print(" TEAMS ALERT - SIMULATION MODE ")
        print("========================================")
        print(f"Title: {title}")
        print(f"Message:\n{message}")
        print("Reason: TEAMS_WEBHOOK_URL is not configured.")

        return False

    payload = {
        "@type": "MessageCard",
        "@context": "https://schema.org/extensions",
        "summary": title,
        "themeColor": "0078D7",
        "title": title,
        "text": message.replace("\n", "<br>"),
    }

    data = json.dumps(
        payload
    ).encode("utf-8")

    request = urllib.request.Request(
        webhook_url,
        data=data,
        headers={
            "Content-Type": "application/json"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(
            request,
            timeout=20
        ) as response:

            success = 200 <= response.status < 300

            print(
                "Teams notification sent successfully."
                if success
                else f"Teams notification returned HTTP {response.status}."
            )

            return success

    except Exception as error:

        print(
            f"Teams notification failed: {error}"
        )

        return False